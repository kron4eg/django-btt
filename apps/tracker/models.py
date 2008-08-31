# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


class Peer(models.Model):
    torrent = models.ForeignKey('torrent.torrent', verbose_name=_('torrent'))
    peer_id = models.CharField(_('peer ID'), max_length=128, db_index=True)
    ip = models.IPAddressField(_('IP address'))
    port = models.PositiveIntegerField(_('post'))
    key = models.CharField(_('key'), max_length=255)
    uploaded = models.PositiveIntegerField(_('uploaded'))
    downloaded = models.PositiveIntegerField(_('downloaded'))
    corrupt = models.PositiveIntegerField(_('corrupt'))
    left = models.PositiveIntegerField(_('left'))
    
    def __unicode__(self):
        return smart_unicode(self.peer_id)

    class Meta:
        verbose_name =_('peer id')
        verbose_name_plural =_('peer ids')
