from django import template
from django.contrib.contenttypes.models import ContentType

from comment.models import Comment
from comment.forms import CommentForm
register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 初始化对应的模型和所在博客的id，方便进行评论
    form = CommentForm(initial={'object_id': obj.pk, 'content_type': content_type.model, 'reply_comment_id': 0})
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None).order_by('-comment_time')
