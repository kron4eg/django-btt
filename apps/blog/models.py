# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.contenttypes import generic
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

class Post(models.Model):
    title = models.CharField(_('title'), max_length=80)
    text = models.TextField(_('text'))
    lang = models.CharField(_('language'), max_length=2, choices=settings.LANGUAGES, db_index=True)
    html = models.TextField(editable=False, blank=True)
    pub_date = models.DateTimeField(_('publication date'))
    upd_date = models.DateTimeField(_('update date'), default=datetime.now)
    published = models.BooleanField(_('published'), default=True)
    tags = TagField(_('tags'))

    def __unicode__(self):
        return smart_unicode(self.title)
    
    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['-pub_date']

    def save(self, force_insert=False, force_update=False):
        from markdown import Markdown
        md = Markdown(extensions=['footnotes'])
        self.html = md.convert(self.text)
        super(Post, self).save(force_insert, force_update)
