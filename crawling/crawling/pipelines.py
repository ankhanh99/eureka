# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import *
from search_engine.models import *

class PagePipeline:
    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            page = Page()
            page.url = item.url
            page.title = item.title
            page.content = item.content
            page.link = item.link
            page.save()
            return page

class PageLinkPipeline:
    def process_item(self, item, spider):
        if isinstance(item, PageLinkItem):
            page_link = PageLink()
            page_link.url = item.url
            page_link.created_at = item.created_at
            page_link.updated_at = item.updated_at
            page_link.save()
            return item

class PageConnectPipeline:
    def process_item(self, item, spider):
        if isinstance(item, PageConnectItem):
            page_connect = PageConnect()
            page_connect.url = item.url
            page_connect.link = item.link
            page_connect.save()
            return item

# class IndexPipeline:
#     def process_item(self, item, spider):
#         if isinstance(item, IndexItem):
#             return item