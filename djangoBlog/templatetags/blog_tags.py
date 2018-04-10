from django.shortcuts import render,get_object_or_404
from django import template
from ..models import Blog,BlogType

#这样才能在html页面中加载该方法
register = template.Library()

@register.simple_tag
def get_categories():
    return BlogType.objects.all()