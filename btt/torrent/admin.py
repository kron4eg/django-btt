# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from torrent.forms import CategoryForm, TorrentForm
from torrent.models import Category, Torrent


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('tree_represent', )
    ordering = ('lft', 'title')

class TorrentAdmin(admin.ModelAdmin):
    form = TorrentForm


admin.site.register(Category, CategoryAdmin)
admin.site.register(Torrent, TorrentAdmin)
