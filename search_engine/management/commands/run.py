from search_engine.indexer import Indexer
from search_engine.pagerank import PageRank
from django.core.management.base import BaseCommand
from django.db.utils import ProgrammingError

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            page_rank = PageRank()
            page_rank.rank()

            indexer = Indexer()
            indexer.index()
            indexer.idf()
            indexer.tfidf()
            indexer.score()
        except ProgrammingError:
            pass