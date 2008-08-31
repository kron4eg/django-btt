# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.contenttypes import generic
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

class Post(models.Model):
    title = models.CharField(_('title'), max_length=80)
    slug = models.SlugField(_('slug'), max_length=80)
    text = models.TextField(_('text'))
    html = models.TextField(editable=False, blank=True)
    pub_date = models.DateTimeField(_('publication date'))
    upd_date = models.DateTimeField(_('update date'), default=datetime.now)
    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return smart_unicode(self.title)
    
    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['-pub_date']
