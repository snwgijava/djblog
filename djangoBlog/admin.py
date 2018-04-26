from django.contrib import admin
from .models import BlogType, Blog, BlogTag


# Register your models here.


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # 字段显示
    list_display = ('id','title','blog_type','author','get_read_num','created_time','last_update_time')
    #搜索
    search_fields = ['title']
    # 筛选
    list_filter = ('created_time','blog_type','blog_tag')

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('id','tag_name')
