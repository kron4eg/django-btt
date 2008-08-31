# -*- coding: utf-8 -*-

from cgi import parse_qsl

from lib import render_to

@render_to('base.html')
def announce(request):
    qs = dict(parse_qsl(request.META['QUERY_STRING']))
    info_hash = qs.get('info_hash').encode('hex')
    return {}
