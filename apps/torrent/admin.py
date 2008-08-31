# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from torrent.models import Category, Torrent

admin.site.register(Category)
admin.site.register(Torrent)
