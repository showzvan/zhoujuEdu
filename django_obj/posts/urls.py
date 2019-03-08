#-*-coding:utf-8-*-

from django.urls import path,re_path
from . import views

app_name='posts'
urlpatterns = [
    path('get_posts/',views.get_posts,name='get_posts'),
    path('del_posts/',views.del_posts,name='del_post'),
    path('get_del_posts/',views.get_del,name='get_del'),
    path('recover_post/',views.recover_post,name='recover_post'),
    path('last_del_post/',views.last_del_post,name='last_del_post'),
    path('add_post/',views.AddPosts.as_view(),name='AddPosts'),
    path('edit_post/',views.EditPost.as_view(),name='EditPost'),
]