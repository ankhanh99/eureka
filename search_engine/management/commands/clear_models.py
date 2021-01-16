from django.core.management.base import BaseCommand
from search_engine.models import *
from django.db.utils import ProgrammingError

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            PageLink.objects.all().delete()
            Page.objects.all().delete()
            PageConnect.obkects.all().delete()
            Index.objects.all().delete()
        except ProgrammingError:
            pass