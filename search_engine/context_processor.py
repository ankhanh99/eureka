import re
import textwrap
from django import template

register = template.Library()


@register.inclusion_tag('search.html')
def get_excerpt(content, q):
    start = 0
    if re.search(q, content, re.IGNORECASE):
        try:
            start = content.lower().index(q.lower())
        except Exception as e:
            print(e)
            pass
    return textwrap.shorten(content[start:], width=150, placeholder="...")