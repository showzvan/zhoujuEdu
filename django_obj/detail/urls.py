#-*-coding:utf-8-*-

from django.urls import path
from . import views

app_name = 'detail'
urlpatterns = [
    path('inner_link/',views.inner_link,name="inner_link"),
    path('add_link/',views.AddLink.as_view(),name="add_link"),
    path('edit_link/',views.EditLink.as_view(),name="edit_link"),
    path('del_link/',views.del_link,name="del_link"),
    path('get_del_links/',views.get_del_links,name="get_del_links"),
    path('recover_link/',views.recover_link,name="recover_link"),
    path('las_del_link/',views.las_del_link,name="las_del_link"),
    path('get_regions/',views.get_regions,name="get_regions"),
    path('add_region/',views.AddRegion.as_view(),name="add_region"),
    path('edit_region/',views.EditRegion.as_view(),name="edit_region"),
    path('del_region/',views.del_region,name="del_region"),
    path('get_del_regions/',views.get_del_regions,name="get_del_regions"),
    path('recover_region/',views.recover_region,name="recover_region"),
    path('las_del_region/',views.las_del_region,name="las_del_region"),
]