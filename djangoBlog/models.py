from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_num = models.IntegerField(default=0)
    created_time = models.DateTimeField()
    last_update_time = models.DateTimeField(auto_now_add=True)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)


    def __str__(self):
        return "<Blog:%s>" % self.title

    class meta:
        order = ['-created_time']



