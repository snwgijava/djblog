from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
class Comment(models.Model):
    #on_delete=models.CASCADE  删除关联数据时不做任何处理
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)

    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
    #回复评论所用的字段
    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['comment_time']


    def __str__(self):
        return self.text
