# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('btt.tracker.views',
    url(r'^$', 'announce', name='announce'),
)
