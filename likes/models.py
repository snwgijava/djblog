from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class LikeCount(models.Model):
    #ContentType用来绑定多个（多态）模型
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    liked_num = models.IntegerField(default=0,verbose_name='点赞数')

    class Meta:
        verbose_name = '点赞数'
        verbose_name_plural = verbose_name

class LikeRecord(models.Model):
    # ContentType用来绑定多个（多态）模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name



