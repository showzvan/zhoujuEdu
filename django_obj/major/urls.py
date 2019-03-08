#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views

app_name='major'
urlpatterns = [
    path("get_major/",views.get_major,name="get_major"),
    path("detail_major/",views.detail_major,name="detail_major"),
    path("delete_major/",views.delete_major,name="delete_major"),
    path("get_del_major/",views.get_del_major,name="get_del_major"),
    path("recover_major/",views.recover_major,name="recover_major"),
    path("las_del_major/",views.las_del_major,name="las_del_major"),
    path("add_major/",views.AddMajor.as_view(),name="AddMajor"),
    path("edit_major/",views.EditMajor.as_view(),name="EditMajor"),
    path("get_cate/",views.get_cate,name="get_cate"),
    path("add_cate/",views.AddCate.as_view(),name="AddCate"),
    path("have_cate/",views.have_cate,name="have_cate"),
    path("edit_cate/",views.EditCate.as_view(),name='EditCate'),
    path("del_cate/",views.del_cate,name='del_cate'),
    path("get_del_cate/",views.get_del_cate,name='get_del_cate'),
    path("recover_cate/",views.recover_cate,name='recover_cate'),
    path("las_del_cate/",views.las_del_cate,name='las_del_cate'),
]


