# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

    url(r'^$', views.my_view, name='my_view'),
    url(r'^login/$', views.Loging_View.as_view(), name='my-login'),   # 默认的登录界面

    url(r'^myview/$', login_required(views.my_view), name='my_view'),     

    
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
    url(r'^login_view/$', views.login_view, name='login_view'),
    url(r'^login_info_show/$', views.login_info_show, name='login_info_show'),
#    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myauth/login.html'}),    
]

