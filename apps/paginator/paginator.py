# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query import QuerySet
from django.http import Http404


def paginate(per_page=settings.PER_PAGE):
    """
    paginate([per_page])

    decorator to make paginate output
    usage:

        @render_to('template_name.html')
        @paginate()
        def your_view(request, ...)
            some_code_here...
            return {'objects': objects_list}

    Keyword arguments:
    per_page -- objects per page
        
        @paginate(per_page=5)
        will output 5 object per page
    
    _paginate_by -- optional key in incomming dict, point decorator to QuerySet    

        @render_to('template_name.html')
        @paginate()
        def some_view(request):
            some_code_here...
            return {'objects': objects_list, '_paginate_by': 'objects'}

    """
    def decorator(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            if '_paginate_by' in output:
                paginate_by = output.get('_paginate_by')
                object_list = output[paginate_by]
            else:
                for key in output:
                    if isinstance(output[key], QuerySet):
                        paginate_by = key
                        object_list = output[paginate_by]
                        break
            paginator = Paginator(object_list, per_page)

            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1

            try:
                output['page'] = paginator.page(page)
                output['object_list'] = output['page'].object_list
                get = request.GET.copy()
                get.pop('page', None)
                output['get_params'] = get.urlencode()
            except InvalidPage:
                raise Http404
            return output
        return wrapper
    return decorator
