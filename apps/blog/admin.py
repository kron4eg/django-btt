# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang', 'published', 'tags', 'pub_date')
    list_filter = ('lang', )
    date_hierarchy = 'pub_date'
    fieldsets = (
        (_('Title'), {'fields': ('title',)}),
        (_('Text'), {'fields': ('text',)}),
        (_('Options'), {'fields': ('lang', 'tags', 'published')}),
        (_('Date'), {'fields': ('pub_date', 'upd_date')}),
    )

admin.site.register(Post, PostAdmin)
