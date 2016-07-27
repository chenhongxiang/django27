# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views 

#  在settings中设置 LOGIN_REDIRECT_URL 为首页URL 
#  https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url

urlpatterns = [
    url(r'^mine/$', login_required(views.MyView.as_view()), name='my-view'),

    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
        
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', login_required(views.ResultsView.as_view()), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', login_required(views.vote), name='vote'),    
]