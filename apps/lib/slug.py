# -*- coding: utf-8 -*-

from django.template.defaultfilters import slugify

TRANS_TABLE = {
    u'а': 'a',
    u'б': 'b',
    u'в': 'v',
    u'г': 'g',
    u'д': 'd',
    u'е': 'e',
    u'ё': 'io',
    u'ж': 'j',
    u'з': 'z',
    u'и': 'i',
    u'й': 'yi',
    u'к': 'k',
    u'л': 'l',
    u'м': 'm',
    u'н': 'n',
    u'о': 'o',
    u'п': 'p',
    u'р': 'r',
    u'с': 's',
    u'т': 't',
    u'у': 'u',
    u'ф': 'f',
    u'х': 'h',
    u'ц': 'ts',
    u'ч': 'ch',
    u'ш': 'sh',
    u'щ': 'shch',
    u'ъ': 'i',
    u'ы': 'i',
    u'ь': 'i',
    u'э': 'ye',
    u'ю': 'u',
    u'я': 'ya',
    u'ă': 'a',
    u'î': 'i',
    u'ţ': 't',
    u'â': 'a',
    u'ş': 's',
    u' ': '-',
}

def slugit(string, enc='utf-8'):
    return slugify(''.join(map(lambda x: TRANS_TABLE.get(x.lower(), x), string)))
