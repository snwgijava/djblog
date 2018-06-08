from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return '<UserProfile:{0} for {1}>'.format(self.nickname,self.user.username)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
