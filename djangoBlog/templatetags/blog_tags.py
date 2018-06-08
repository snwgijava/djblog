from django.shortcuts import render,get_object_or_404
from django import template
from django.db.models import Count, Sum

from read_views.models import ReadNum
from ..models import Blog, BlogType, BlogTag

#这样才能在html页面中加载该方法
register = template.Library()

#分类归档
@register.simple_tag
def get_categories():
    return BlogType.objects.annotate(num_blog_types=Count('blog'))

#日期
@register.simple_tag
def archives():
    return Blog.objects.dates('created_time','month',order='DESC')

#标签云
@register.simple_tag
def get_tags():
    return BlogTag.objects.annotate(num_blog_tags=Count('blog')).filter(num_blog_tags__gt=0)


@register.simple_tag
def get_view_nums():
    view_nums = ReadNum.objects.aggregate(Sum('read_num'))
    return view_nums['read_num__sum']