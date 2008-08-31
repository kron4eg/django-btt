# -*- coding: utf-8 -*-

from django import template

from blog.models import Post

register = template.Library()

@register.filter
def undercat(value, len=None):
    bits = value.split('<!--break-->')
    if bits.__len__() == 2:
        return '%s' % (bits[0])
    return value

@register.inclusion_tag('blog/post_list.html', takes_context=True)
def blog_short_list(context, count=5):
    lang = context['request'].LANGUAGE_CODE
    post_list = Post.objects.filter(published=True, lang=lang)[:count]
    return {'post_list': post_list}
