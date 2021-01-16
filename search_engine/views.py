from functools import reduce

import math
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
import re
import operator
from django.db.models import Q
import time

# Create your views here.
from search_engine.models import Index

def index(request):
    return render(request, 'index.html')

def search(request):
    start_time = time.time()
    pages = None
    page_count = 0
    pagination_data = None
    q = request.GET.get('q', default=None)
    p = int(request.GET.get('p', default=1))

    if q != None and q.strip() != '':
        # search
        q = re.sub(' +', ' ', q)
        words = re.sub('(\'s|\'|\")', '', q.lower()).split()
        per_page = 15
        query = reduce(operator.and_, (Q(word = item) for item in words))
        obj_list = list(Index.objects.filter(query).distinct('page'))

        if not obj_list:
            pages = []
            page_count = 0
        else:
            paginator = Paginator(obj_list, per_page)
            try:
                pages = paginator.page(p).object_list
            except EmptyPage:
                pages = paginator.page(1).object_list
            page_count = len(obj_list)

        #pagination to return items in the front end
        last_page= math.ceil(page_count / per_page)
        start_page = p - 2 if (p - 2) > 0 else 1
        end_page = p + 2 if (p + 2) < last_page else last_page
        pagination_data = {
            'start_page': start_page,
            'end_page': end_page,
            'last_page': last_page,
        }

    search_time = time.time() - start_time

    context = {
        'pagination_data': pagination_data,
        'pages': pages,
        'pages_count': page_count,
        'q': q,
        'p': p,
        'previous': p-1,
        'next': p+1,
        'search_time': search_time,
        'range': range(pagination_data['start_page'], pagination_data['end_page'] + 1),
    }

    return render(request, 'search.html', context)
