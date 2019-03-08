#-*-coding:utf-8-*-
from django.urls import path
from . import views

app_name = 'cms'
urlpatterns = [
    path('',views.IndexView.as_view(),name = 'index'),
    path('login/',views.LoginView.as_view(),name = 'login'),
    path('logout/',views.logout,name = 'logout'),
]
