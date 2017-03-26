"""ctd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','ncc.views.home'),
    url(r'^about/$','ncc.views.about'),
    url(r'^team/$','ncc.views.showteam'),
    url(r'^signup$','ncc.views.signup'),
    url(r'^question/(?P<question_id>[0-9]+)/back$','ncc.views.return_editor_page'), #getmethod
    url(r'^question/(?P<question_id>[0-9]+)/$','ncc.views.question_list'),  #get method
    url(r'^question/(?P<question_id>[0-9]+)/result$','ncc.views.code_test'), #get method
    url(r'^leaderboard/$','ncc.views.leaderboard'),
    url(r'^log_out$','ncc.views.log_out'),
    url(r'^questionlist/$','ncc.views.question_view'),
    url(r'^login$','ncc.views.call_login_page'),  
    url(r'^callingloginpage$','ncc.views.log_in'),
    url(r'^time/','ncc.views.timer'),       
    url(r'^questionlist/log_out$','ncc.views.leaderboard'),
]
