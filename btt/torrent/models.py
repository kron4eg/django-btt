# -*- coding: utf-8 -*-

from hashlib import sha1

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from treebeard.mp_tree import MP_Node

from btt.lib import bencoding


class Category(MP_Node):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Parent'))
    title = models.CharField(_('Title'), max_length=80)
    image = models.ImageField(_('Image'), upload_to='img/category', blank=True, null=True)
    count = models.PositiveIntegerField(editable=False, default=0)
    
    def __unicode__(self):
        return smart_unicode(self.title)

#    def tree_represent(self, space='&nbsp;', begin_from_level=0):
#        return space * 4 * (self.level - begin_from_level) + ' %s' % self.__unicode__()
#    tree_represent.allow_tags = True

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Torrent(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(_('Title'), max_length=80)
    author = models.ForeignKey('auth.user', blank=True, null=True, verbose_name=_('Author'))
    image = models.ImageField(_('Image'), upload_to='img/torrents', blank=True, null=True)
    text = models.TextField(_('Text'))
    html = models.TextField(editable=False, blank=True)

    torrent = models.TextField(editable=False)
    info_hash = models.CharField(_('Info hash'), max_length=40, db_index=True, editable=False)
    files = models.PositiveIntegerField(editable=False)
    size = models.PositiveIntegerField(editable=False)
    seeders = models.PositiveIntegerField(editable=False, default=0)
    leechers = models.PositiveIntegerField(editable=False, default=0)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    comment_count = models.PositiveIntegerField(editable=False, default=0)
    comments_enabled = models.BooleanField(_('comments enabled'), default=True)
    
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
