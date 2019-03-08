#-*-coding:utf-8-*-
from django.urls import path
from . import views
from . views import ForCodeView

app_name = 'users'
urlpatterns = [
    path('myenter/',views.userEnter,name='userEnter'),
    path('agreement/',views.agreement,name='agreement'),
    path('forcode/',ForCodeView.as_view(),name='forcode'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.logOut,name='logout'),
]