from django.contrib import admin
from .models import *

# Register your models here.
class PageLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'created_at', 'updated_at')

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'content', 'pagerank', 'created_at', 'last_indexed')

class PageConnectAdmin(admin.ModelAdmin):
    list_display = ('url', 'link')

class IndexAdmin(admin.ModelAdmin):
    list_display = ('page', 'word', 'tf', 'idf', 'tfidf', 'score', 'last_idf', 'last_tfidf', 'last_scored')


admin.site.register(PageLink, PageLinkAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageConnect, PageConnectAdmin)
admin.site.register(Index, IndexAdmin)