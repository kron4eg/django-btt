# -*- coding: utf-8 -*-

import pickle
from hashlib import sha1

from django import forms
from django.utils.translation import ugettext_lazy as _

from lib.bt.bencoding import encode, decode, InvalidDataError
from sorl.thumbnail.main import DjangoThumbnail
from torrent.fields import AdminImageWidget
from torrent.models import Category, Torrent


class CategoryChoice(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        self.begin_from_level = kwargs.pop('begin_from_level', 0)
        super(CategoryChoice, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.tree_represent(space='-', begin_from_level=self.begin_from_level)


class CategoryForm(forms.ModelForm):
    parent = CategoryChoice(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(level__in=[0,1])
    
    class Meta:
        model = Category


class TorrentForm(forms.ModelForm):
    category = CategoryChoice(queryset=Category.objects.all(), empty_label=None, begin_from_level=1)
    torrent = forms.FileField()
    image = forms.FileField(widget=AdminImageWidget, label=_('image'), required=False)

    def __init__(self, *args, **kwargs):
        super(TorrentForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(level=0)

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
