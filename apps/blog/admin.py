# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'pub_date', 'published')
    date_hierarchy = 'pub_date'
    fieldsets = (
        (_('Title'), {'fields': (('title', 'slug'),)}),
        (_('Text'), {'fields': ('text', 'published')}),
        (_('Date'), {'fields': ('pub_date', 'upd_date')})
    )

admin.site.register(Post, PostAdmin)
