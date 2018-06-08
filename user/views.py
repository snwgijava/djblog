from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from . forms import LoginForm,RegForm,ChangeNickNameForm
from .models import UserProfile
# Create your views here.


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
            if not request.GET.get('from'):
                return redirect('home')
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    content = {}
    content['login_form'] = login_form
    return render(request,'user/login.html',content)

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
            if not request.GET.get('from'):
                return redirect('home')
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegForm()
    content = {}
    content['register_form'] = register_form
    return render(request,'user/register.html',content)

def logout(request):
    auth.logout(request)
    if not request.GET.get('from'):
        return redirect('home')
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    return render(request,'user/user_info.html')

def change_nickname(request):
    redirect_to = request.GET.get('form',reverse('home'))
    if request.method == 'POST':
        form = ChangeNickNameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            user_profile,created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.nickname = nickname_new
            user_profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNickNameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    return render(request,'form.html',context)
