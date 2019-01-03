__author__ = 'yangjian'
__date__ = '2018/6/13 22:34'

from django.forms import ModelForm
from djangoBlog.models import Blog


class NewBlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content','blog_type','blog_tag']



