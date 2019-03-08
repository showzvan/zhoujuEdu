#-*-coding:utf-8-*-
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('get_order/',views.order_list,name='order_list'),
    path('delete_order/',views.delete_order,name='delete_order'),
    path('get_del_order/',views.get_del,name='get_del'),
    path('recover_order/',views.re_order,name='re_order'),
    path('las_del_order/',views.las_del_order,name='las_del_order'),
    path('detail_order/',views.detail_order,name='detail_order'),
    path('add_order/',views.AddOrder.as_view(),name='AddOrder'),
    path('have_major/',views.have_major,name='have_major'),
    path('edit_order/',views.EditOrder.as_view(),name='EditOrder'),
]
