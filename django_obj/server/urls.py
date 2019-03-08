#-*-coding:utf-8-*-
from django.urls import path
from . import views

app_name = 'server'

urlpatterns = [
    path('server_posts/',views.server_posts,name='server_posts'),
    path('add_server_post/',views.AddServerPost.as_view(),name='add_server_post'),
    path('edit_server_post/',views.EditServerPost.as_view(),name='edit_server_post'),
    path('del_server_posts/',views.del_ser_pos,name='del_ser_pos'),
    path('del_server_posts_list/',views.del_ser_list,name='del_ser_list'),
    path('recover_server/',views.recover_server,name='recover_server'),
    path('las_del_posts/',views.las_del_posts,name='las_del_posts'),
    path('server_cate/',views.server_cate,name='server_cate'),
    path('add_cate/',views.AddCate.as_view(),name='AddCate'),
    path('edit_cate/',views.EditCate.as_view(),name='edit_cate'),
    path('del_cate/',views.del_cate,name='del_cate'),
    path('get_del_cate/',views.get_del_cate,name='get_del_cate'),
    path('recover_cate/',views.recover_cate,name='recover_cate'),
    path('las_del_cate/',views.las_del_cate,name='las_del_cate'),
    path('center/',views.center,name='center'),
    path('add_center/',views.AddCenter.as_view(),name='add_center'),
    path('edit_center/',views.EditCenter.as_view(),name='edit_center'),
    path('delete_center/',views.delete_center,name='delete_center'),
    path('del_center_list/',views.del_center_list,name='del_center_list'),
    path('recover_center/',views.recover_center,name='recover_center'),
    path('last_del_center/',views.last_del_center,name='last_del_center'),
    path('get_enclosure/',views.get_enclosure,name='get_enclosure'),
    path('get_file/',views.get_file,name='get_file'),
    path('add_enclo/',views.AddEnclosure.as_view(),name='AddEnclo'),
    path('edit_enclosure/',views.EditEnclosure.as_view(),name='edit_enclosure'),
    path('del_enclosure/',views.del_enclosure,name='del_enclosure'),
    path('get_del_enclosure/',views.get_del_enclosure,name='get_del_enclosure'),
    path('recover_enclosure/',views.recover_enclosure,name='recover_enclosure'),
    path('las_del_enclosure/',views.las_del_enclosure,name='las_del_enclosure'),
    path('add_quest/',views.AddQuest.as_view(),name='add_quest'),
    path('edit_quest/',views.EditQuest.as_view(),name='edit_quest'),
    path('del_quest/',views.del_quest,name='del_quest'),
    path('get_del_files/',views.get_del_files,name='get_del_files'),
    path('recover_quest/',views.recover_quest,name='recover_quest'),
    path('las_del_quest/',views.las_del_quest,name='las_del_quest'),
]