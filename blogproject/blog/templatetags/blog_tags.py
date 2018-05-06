# -*- coding: utf-8 -*-

from ..models import Post,Category
from django import template


register=template.Library()


@register.simple_tag
def get_recent_posts(num=6):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'day', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()