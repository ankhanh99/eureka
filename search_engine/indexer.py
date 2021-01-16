from search_engine.models import *
from django.utils import timezone
from collections import Counter
import datetime
import math
import re


class Indexer():
    def __init__(self):
        self.PAGE_LIMIT = 150

    def index(self):
        pages = Page.objects.order_by('last_indexed')[:self.PAGE_LIMIT]
        for page in pages:
            content = re.sub(r'[^a-zA-Z0-9_\-\' ]+', '', page.content)
            content_list = content.lower().split(' ')
            content_word_count = len(content_list)
            words = Counter(content_list)
            for word, count in words.items():
                tf = count / content_word_count
                try:
                    word = Index.objects.get(page=page, word=word)
                    word.tf = tf
                except (AttributeError, Index.DoesNotExist):
                    Index(page=page, word=word, tf=tf).save()
            page.save()

    def idf(self):
        words = Index.objects.order_by('last_idf').values('word').distinct()
        pages_count = Page.objects.count()

        for word in words:
            item = Index.objects.filter(word=word['word'])  #list all pages that have the matching word
            word_frequency = item.count()
            Index.objects.filter(word=word['word']).update(idf=math.log(pages_count/word_frequency), last_idf=datetime.datetime.now(tz=timezone.utc))

    def tfidf(self):
        index = Index.objects.order_by('last_tfidf')
        for index_record in index:
            tfidf = index_record.tf * index_record.idf
            last_tfidf = datetime.datetime.now(tz=timezone.utc)
            Index.objects.filter(page=index_record.page, word=index_record.word).update(tfidf=tfidf, last_tfidf=last_tfidf)

    def score(self):
        index = Index.objects.order_by('last_scored')
        max_tfidf = Index.objects.order_by("-tfidf").values('tfidf').first()['tfidf']
        max_pagerank = Page.objects.order_by("-pagerank").values('pagerank').first()['pagerank']
        for index_record in index:
            # tfidf = 70%, pagerank = 30%
            tfidf_score = (index_record.tfidf / max_tfidf) * 0.7 if max_tfidf > 0 else 0.7
            pagerank_score = (index_record.page.pagerank / max_pagerank) * 0.3 if max_pagerank > 0 else 0.3
            score = tfidf_score + pagerank_score
            last_scored = datetime.datetime.now(tz=timezone.utc)
            Index.objects.filter(page=index_record.page, word=index_record.word).update(score=score,
                                                                                        last_tfidf=last_scored)