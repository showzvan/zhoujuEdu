#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views


app_name = 'news'
urlpatterns = [
    path('',views.news,name='news'),
    path('news_detail/p=<int:posts_id>',views.news_detail,name='news_detail'),
]