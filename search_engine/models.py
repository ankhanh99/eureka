from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class PageLink(models.Model):
    url = models.TextField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now(tz=timezone.utc)
        self.updated_at = datetime.datetime.now(tz=timezone.utc)
        return super(PageLink, self).save(*args, **kwargs)



class Page(models.Model):
    url = models.TextField(primary_key=True)
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    pagerank = models.FloatField(default=0)
    created_at = models.DateTimeField()
    last_indexed = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now(tz=timezone.utc)
        self.last_indexed = datetime.datetime.now(tz=timezone.utc)
        return super(Page, self).save(*args, **kwargs)

class PageConnect(models.Model):
    url = models.ForeignKey(Page, on_delete=models.CASCADE)
    link = models.ForeignKey(PageLink, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('url', 'link', )


class Index(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    word = models.TextField()
    tf = models.FloatField(default=0)
    idf = models.FloatField(default=0)
    tfidf = models.FloatField(default=0)
    score = models.FloatField(default=0)
    last_idf = models.DateTimeField(default=timezone.now)
    last_tfidf = models.DateTimeField(default=timezone.now)
    last_scored = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('page', 'word'), )