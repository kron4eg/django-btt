# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from torrent.forms import TorrentForm
from torrent.models import Category, Torrent

class TorrentAdmin(admin.ModelAdmin):
    form = TorrentForm


admin.site.register(Category)
admin.site.register(Torrent, TorrentAdmin)
