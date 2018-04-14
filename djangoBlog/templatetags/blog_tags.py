from django.shortcuts import render,get_object_or_404
from django import template
from django.db.models import Count
from ..models import Blog,BlogType

#这样才能在html页面中加载该方法
register = template.Library()

@register.simple_tag
def get_categories():
    return BlogType.objects.annotate(num_blog_types=Count('blog'))

@register.simple_tag
def archives():
    return Blog.objects.dates('created_time','month',order='DESC')