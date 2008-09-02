# -*- coding: utf-8 -*-

from hashlib import sha1

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

import mptt
from lib.bt.bencoding import encode, decode
from tagging.fields import TagField


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    title = models.CharField(_('title'), max_length=80)
    image = models.ImageField(_('image'), upload_to='img/category', blank=True, null=True)
    count = models.PositiveIntegerField(editable=False, default=0)
    
    def __unicode__(self):
        return smart_unicode(self.title)

    def tree_represent(self, space='&nbsp;', begin_from_level=0):
        return space * 4 * (self.level - begin_from_level) + ' %s' % self.__unicode__()
    tree_represent.allow_tags = True

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('lft', 'title')

mptt.register(Category,order_insertion_by=['title'])


class Torrent(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(_('title'), max_length=80)
    author = models.ForeignKey('auth.user', blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='t')
    text = models.TextField(_('text'))
    html = models.TextField(editable=False, blank=True)

    torrent = models.TextField(editable=False)
    info_hash = models.CharField(_('info hash'), max_length=40, db_index=True, editable=False)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    comment_count = models.PositiveIntegerField(editable=False, default=0)
    comments_enabled = models.BooleanField(_('comments enabled'), default=True)
    tags = TagField(_('tags'))
    
    def __unicode__(self):
        return smart_unicode(self.title)

    class Meta:
        verbose_name =_('torrent')
        verbose_name_plural =_('torrents')

    def save(self, force_insert=False, force_update=False):
        from markdown import Markdown
        md = Markdown(extensions=['footnotes'], safe_mode=True)
        self.html = md.convert(self.text)
        super(Torrent, self).save(force_insert, force_update)
