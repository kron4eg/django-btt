# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('tracker.views',
    url(r'^$', 'announce', name='announce'),
)
