#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views


app_name='school'
urlpatterns = [
    path('get_school/',views.get_school,name='get_school'),
    path('edit_school/',views.EditSchool.as_view(),name='EditSch'),
    path('detail_sch/',views.detail_sch,name='detail_sch'),
    path('delete_sch/',views.delete_sch,name='delete_sch'),
    path('get_del_school/',views.get_del_sch,name='get_del_sch'),
    path('recover_school/',views.recover_sch,name='recover_sch'),
    path('las_del_school/',views.las_del_sch,name='las_del_sch'),
    path('add_school/',views.AddSchool.as_view(),name='add_school'),
    path('get_type/',views.get_type,name='get_type'),
    path('add_type/',views.AddType.as_view(),name='AddType'),
    path('delete_type/',views.del_type,name='del_type'),
    path('get_del_type/',views.get_del_type,name='get_del_type'),
    path('recover_type/',views.recover_type,name='recover_type'),
    path('las_del_type/',views.las_del_type,name='las_del_type'),
    path('edit_type/',views.EditType.as_view(),name='EditType'),
    path('get_feature/',views.get_feature,name='get_feature'),
    path('add_feature/',views.AddFeature.as_view(),name='add_feature'),
    path('edit_feature/',views.EditFeature.as_view(),name='edit_feature'),
    path('delete_feature/',views.delete_feature,name='delete_feature'),
    path('get_del_feature/',views.get_del_feature,name='get_del_feature'),
    path('recover_feature/',views.recover_feature,name='recover_feature'),
    path('las_del_feature/',views.las_del_feature,name='las_del_feature'),
]