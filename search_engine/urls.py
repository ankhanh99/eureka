from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*15)(views.index), name='index'),
    path('search/', cache_page(60*15)(views.search), name='search')
]