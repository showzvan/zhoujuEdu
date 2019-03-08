#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views

app_name = 'enter'
urlpatterns = [
    path('',views.enter,name="enter"),
    path('pay/',views.enterPay,name='enterPay'),
    path('pay_success/',views.pay_success,name='pay_success'),
    path('order_pay/',views.ORderPay.as_view(),name="order_pay")
]