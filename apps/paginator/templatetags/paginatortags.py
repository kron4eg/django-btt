# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('paginator/paginator.html', takes_context=True)
def paginator(context):
    page = context['page']
    paginator = page.paginator
    width = 3
    border = 3

    start = max(1, page.number - width)
    end = min(page.number + width, paginator.num_pages)
    page_range = range(start, end+1)

    start_range = range(1, min(paginator.num_pages+1, border+1))
    end_range = range(max(1, paginator.num_pages-(border-1)), paginator.num_pages+1)

    if set(start_range).intersection(page_range):
        page_range = list(set(start_range).union(page_range))
        start_range = None

    if set(page_range).intersection(end_range):
        page_range = list(set(page_range).union(end_range))
        end_range = None

    page_range.sort()

    return {
            'page': page,
            'start': start,
            'end': end,
            'page_range': page_range,
            'start_range': start_range,
            'end_range': end_range,
            'path': context['request'].path,
            'get_params': context['get_params'],
    }
