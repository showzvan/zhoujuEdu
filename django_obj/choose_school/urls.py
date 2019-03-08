#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views


app_name='choose_school'
urlpatterns = [
    path('',views.school,name='school'),
    path('intro/i=<int:school_id>',views.school_intro,name='school_intro'),
    path('detail/d=<int:school_id>',views.school_detail,name='school_detail'),
]