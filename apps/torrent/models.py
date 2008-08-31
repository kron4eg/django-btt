# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField


class Category(models.Model):
    title = models.CharField(_('title'), max_length=80)
    slug = models.SlugField(_('slug'), max_length=80)
    image = models.ImageField(_('image'), upload_to='c')
    count = models.PositiveIntegerField(editable=False)
    
    def __unicode__(self):
        smart_unicode(self.title)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['title']


class Torrent(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(_('title'), max_length=80)
    image = models.ImageField(_('image'), upload_to='t')
    info_hash = models.CharField(_('info hash'), max_length=40, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    comment_count = models.PositiveIntegerField(editable=False)
    comments_enabled = models.BooleanField(_('comments enabled'), default=True)
    tags = TagField(_('tags'))
    
    def __unicode__(self):
        smart_unicode(self.title)

    class Meta:
        verbose_name =_('torrent')
        verbose_name_plural =_('torrents')
