from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20,verbose_name='昵称')
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100,verbose_name='头像')

    def __str__(self):
        return '<UserProfile:{0} for {1}>'.format(self.nickname,self.user.username)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

def get_nickname(self):
    if UserProfile.objects.filter(user=self).exists():
        userprofile = UserProfile.objects.get(user=self)
        return userprofile.nickname
    else:
        return ''

def get_nickname_or_username(self):
    if UserProfile.objects.filter(user=self).exists():
        userprofile = UserProfile.objects.get(user=self)
        return userprofile.nickname
    else:
        return self.username

def has_nickaname(self):
    return UserProfile.objects.filter(user=self).exists()

User.get_nickname = get_nickname
User.has_nickname = has_nickaname
User.get_nickname_or_username = get_nickname_or_username
