#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views

app_name = 'about'
urlpatterns = [
    path('index/',views.index,name = 'about_index'),
    path('contact/',views.contact,name = 'contact'),
    path('fv/',views.fv,name = 'about_fv'),
    path('agreement/',views.agreement,name = 'about_agreement'),
    path('links/',views.links,name = 'about_links'),
]