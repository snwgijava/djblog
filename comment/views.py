from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment
# Create your views here.

def update_commnet(request):
    '''referer = request.META.get('HTTP_REFERER', reverse('home'))
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
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)'''
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST,user=request.user)
    data = {}
    if comment_form.is_valid():
        #检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        #判断回复的是不是评论
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        #返回json数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        #评论用户的头像
        data['comment_user_image'] = comment.user.userprofile.image.url
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        #回复用户的头像
        data['reply_user_image'] = comment.reply_to.userprofile.image.url
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)


