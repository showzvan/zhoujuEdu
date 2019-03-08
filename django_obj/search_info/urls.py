#-*-coding:utf-8-*-
from django.urls import path
from . import views

app_name = 'search_info'
urlpatterns = [
    path('search/',views.search,name='search'),
    path('search_school/',views.searchSchool,name='search_school'),
    path('search_major/',views.searchMajor,name='search_major'),
    path('search_center/',views.searchCenter,name='search_center'),
    path('search_news/',views.searchNews,name='search_news'),
]