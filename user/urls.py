__author__ = 'yangjian'
__date__ = '2018/5/29 21:46'

from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_for_model/', views.login_model_form, name='login_for_model'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/',views.change_nickname,name='change_nickname'),
    path('bind_email/',views.bind_email,name='bind_email'),
    path('send_verifcation_code/',views.send_verifcation_code,name='send_verifcation_code'),
    path('update_info/<int:pk>',views.UpdateUserInfoView.as_view(),name='update_info'),
]