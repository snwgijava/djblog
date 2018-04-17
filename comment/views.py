from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Comment
# Create your views here.

def update_commnet(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    #数据检查
    if not request.user.is_authenticated:
        return render(request,'error.html',{'message':'用户未登录','redirect_to':referer})
    text = request.POST.get('text','').strip()
    if text == '':
        return render(request,'error.html',{'message':'评论不对为空','redirect_to':referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()  # 得到blog这个类型
        model_obj = model_class.objects.get(pk=object_id)  # 获取到博客文章id
    except Exception as e:
        return render(request,'error.html',{'message':'评论对像不存在','redirect_to':referer})

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    return redirect(referer)
