import string,random,time
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.views.generic import UpdateView

from . forms import LoginForm,RegForm,ChangeNickNameForm,BindEmailForm
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
            UserProfile.objects.create(user=user)

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
    context['return_back_url'] = redirect_to
    return render(request,'form.html',context)

class UpdateUserInfoView(UpdateView):
    model = UserProfile
    fields = ['nickname','image']
    template_name = 'blog/blog_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '修改个人信息'
        context['button'] = '修改'
        return context

def bind_email(request):
    redirect_to = request.GET.get('form', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()


    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verifcation_code(request):
    email = request.GET.get('email','')

    data = {}
    if email != '':
        #生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits,4))
        #发送邮件间隔30秒
        now = int(time.time())
        send_code_time = int(request.session.get('send_code_time','0'))
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

        #发送邮件
        send_mail('绑定邮箱','验证码：{0}'.format(code),'809127232@qq.com',[email],fail_silently=False,)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
