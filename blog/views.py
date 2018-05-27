import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache

from djangoBlog.models import Blog
from read_views.utls import get_seven_days_read_data,get_today_hot_data
from . forms import LoginForm,RegForm


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gt=date)\
        .values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')[:7]
    return blogs


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)

    #获取七天热门文章的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_data_for_7_days',hot_data_for_7_days,3)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_date'] = get_today_hot_data(blog_content_type)
    context['hot_data_for_7_days'] = hot_data_for_7_days
    return render_to_response('home.html',context)

def login(request):
    '''username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request,username=username,password=password)
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    if user is not None:
        auth.login(request,user)
        return redirect(referer)
    else:
        return '用户名或密码不正确'''''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()
    content = {}
    content['login_form'] = login_form
    return render(request,'login.html',content)

def login_model_form(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        register_form = RegForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username,email,password)
            user.save()

            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password)
            # user.save()

            #登录用户
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        register_form = RegForm()
    content = {}
    content['register_form'] = register_form
    return render(request,'register.html',content)