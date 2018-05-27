from django.contrib import admin

# Register your models here.
from likes.models import LikeCount,LikeRecord


@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id','content_type','object_id','content_object','liked_num')

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id','content_type','object_id','content_object','user','liked_time')

