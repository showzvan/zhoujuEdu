#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views

app_name = 'choose_major'
urlpatterns = [
    path('',views.choose_major,name = 'choose_major'),
    path('<int:major_pk>&<int:school_pk>',views.major_detail,name = 'major_detail'),
    path('get_major/',views.major_school,name = 'major_school'),
    path('get_school/',views.level_school,name = 'level_school'),
]