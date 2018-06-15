from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.urls import reverse

from read_views.models import ReadNum, ReadNumExpandMethod,ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15,verbose_name='分类')

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name

class BlogTag(models.Model):
    tag_name = models.CharField(max_length=15,verbose_name='标签')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name


class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    content = RichTextUploadingField(verbose_name='文章内容')
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE,verbose_name='文章分类')
    blog_tag = models.ManyToManyField(BlogTag,verbose_name='标签')
    read_details = GenericRelation(ReadDetail,verbose_name='阅读记录')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name
        # order = ['-created_time']


    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})




