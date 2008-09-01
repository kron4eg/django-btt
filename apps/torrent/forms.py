# -*- coding: utf-8 -*-

import pickle
from hashlib import sha1

from django import forms
from django.utils.translation import ugettext_lazy as _

from lib.bt.bencoding import encode, decode, InvalidDataError
from torrent.models import Torrent


class TorrentForm(forms.ModelForm):
    
    torrent = forms.FileField()

    class Meta:
        model = Torrent
   
    def clean_torrent(self):
        if not self.cleaned_data['torrent'].multiple_chunks():
            try:
                self.decoded = decode(self.cleaned_data['torrent'].read())
                return self.cleaned_data['torrent']
            except InvalidDataError:
                raise forms.ValidationError(_(u'Not a torrent file.'))
        else:
            raise forms.ValidationError(_('File too big for torrent file'))


    def save(self, commit=True):
        self.instance.torrent = pickle.dumps(self.decoded)
        self.instance.info_hash = sha1(encode(self.decoded['info'])).hexdigest()
        fail_message = 'created' if self.instance.pk is None else 'changed'
        return forms.save_instance(self, self.instance, self._meta.fields, fail_message, commit)
