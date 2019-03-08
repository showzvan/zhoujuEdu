# -*-coding:utf-8-*-
from django.urls import path,re_path
from . import views

app_name = "user"
urlpatterns = [
    path('', views.indexList, name="IndexList"),
    path('add_user/', views.AddUserView.as_view(), name="AddUser"),
    path('delete_user/', views.delete_user, name="delete_user"),
    path('delete_user_list/', views.delete_user_list, name="delete_user_list"),
    path('recover_user/', views.recover_user, name="recover_user"),
    path('last_delete_user/', views.last_delete_user, name="last_delete_user"),
    path('edit_user/', views.EditUser.as_view(), name="edit_user"),
    path('user_info/', views.user_info, name="user_info"),
    path('get_city/', views.get_city, name='get_city'),
    path('get_city/', views.get_city, name='get_city'),
    path('get_country/', views.get_country, name='get_country'),
    path('edit_pwd/', views.EditPwd.as_view(), name='edit_pwd'),
    path('detail_user/', views.detail_user, name='detail_user'),
    path('upload/', views.UserImageUpload.as_view(), name='upload'),
    path('restart_pwd/', views.RestartPwd.as_view(), name='restart_pwd'),
    re_path('active/(?P<active_code>.*)/',views.change_pwd,name='active'),
    path('modiffed/',views.resetPwd,name = 'reset_pwd'),
    path('admin_list/',views.admin_list,name='get_admin'),
    path('delete_admin/',views.delete_admin,name='delete_admin'),
    path('get_delete_admin/',views.delete_admin_list,name='delete_admin_list'),
    path('recover_admin/',views.recover_admin,name='recover_admin'),
    path('last_delete_admin/',views.last_delete_admin,name='last_admin'),
    path('add_admin/',views.AddAdmin.as_view(),name='add_admin'),
    path('edit_admin_pwd/',views.EditAdPwd.as_view(),name='EditAdPwd'),
    path('admin_upload/',views.AdUpload.as_view(),name='AdUpload'),

]
