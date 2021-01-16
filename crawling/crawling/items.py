# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from search_engine.models import *

# class IndexItem(DjangoItem):
#     django_model = Index
#     page = scrapy.Field()
#     word = scrapy.Field()
#     tf = scrapy.Field()
#     idf = scrapy.Field()
#     tfidf = scrapy.Field()
#     score = scrapy.Field()
#     last_idf = scrapy.Field()
#     last_tfidf = scrapy.Field()
#     last_score = scrapy.Field()
#
#     objects = models.Manager()


class PageItem(DjangoItem):
    django_model = Page
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()

    objects = models.Manager()


class PageLinkItem(DjangoItem):
    django_model = PageLink
    url = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()

    objects = models.Manager()


class PageConnectItem(DjangoItem):
    url = scrapy.Field()
    link = scrapy.Field()

    objects = models.Manager()

