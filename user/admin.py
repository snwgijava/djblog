from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

#
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    #不允许删除
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username','nickname','email','is_staff','is_active','is_superuser')

    def nickname(self,obj):
        return obj.userprofile.nickname
    nickname.short_description = '昵称'

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nickname')

