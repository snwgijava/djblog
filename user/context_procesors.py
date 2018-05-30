__author__ = 'yangjian'
__date__ = '2018/5/29 21:57'

from .forms import LoginForm


#这里的作用是替换掉自带的from,需要在setting中添加
def login_model_form(request):
    return {'login_model_form':LoginForm}