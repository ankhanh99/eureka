from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import *
from scrapy.selector import Selector
import lxml
from lxml.html.clean import Cleaner
import re
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.transaction import TransactionManagementError

class WebSpider(CrawlSpider):
    name = 'web_spider'
    allowed_domains = []
    start_urls = ['http://cnn.com/', 'http://bbc.com/', 'http://amazon.com/', 'https://amazon.com/', 'https://bbc.com/', 'https://cnn.com/']
    rules = [Rule(LinkExtractor(),
                  callback='parse', follow=True, errback='handle_error')]

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 100,
        'CONCURRENT_REQUESTS': 100,
        'CLOSESPIDER_ITEMCOUNT': 100
    }

    def handle_error(self, failure):
        print("Request failed: %s" % failure.request)

    def parse(self, response):
        selector = Selector(response)
        # get page title
        page_title = selector.xpath('//title/text()').extract()[0]
        # get page content
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        page_html = selector.xpath('//body').extract()[0]
        # remove js and css code
        page_html = cleaner.clean_html(page_html)
        # extract text
        html_doc = lxml.html.document_fromstring(page_html)
        page_content = ' '.join(lxml.etree.XPath("//text()")(html_doc))
        page_content += ' ' + page_title
        # remove line breaks, tabs and extra spaces
        page_content = re.sub('\n', ' ', page_content)
        page_content = re.sub('\r', ' ', page_content)
        page_content = re.sub('\t', ' ', page_content)
        page_content = re.sub(' +', ' ', page_content)
        page_content = page_content.strip()
        # get page links
        page_hrefs = response.xpath('//a/@href').extract()
        page_urls = []
        # filter out links with unallowed domains
        for link in page_hrefs:
            # convert relative links to absolute urls
            url = response.urljoin(link)
            page_urls.append(url)

        # save the page
        with transaction.atomic():
            try:
                obj = PageItem.objects.get(url=response.url)
                obj.title = page_title
                obj.content = page_content
                obj.save()
            except ObjectDoesNotExist:
                obj = PageItem.objects.create(url=response.url, title=page_title, content=page_content)
            except AttributeError:
                obj = PageItem(url=response.url, title=page_title, content=page_content).save()

            for url in page_urls:
                try:
                    PageConnect(url=obj, link=PageLinkItem(url=url).save()).save()
                except (IntegrityError, TransactionManagementError):
                    continue