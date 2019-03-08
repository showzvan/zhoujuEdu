"""django_obj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.static import serve
from django.urls import path,include,re_path
from django.conf.urls import url
from django_obj import settings
from home.views import home

urlpatterns = [
    path('',home,name='home'),
    path('about/',include('about.urls')),
    path('choose_major/',include('choose_major.urls')),
    path('choose_school/',include('choose_school.urls')),
    path('news/',include('news.urls')),
    path('service/',include('service.urls')),
    path('cms/',include('cms.urls')),
    path('user/',include('user.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('school/',include('school.urls')),
    path('major/',include('major.urls')),
    path('order/',include('order.urls')),
    path('posts/',include('posts.urls')),
    path('server/',include('server.urls')),
    path('detail/',include('detail.urls')),
    path('enter/',include('enter.urls')),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    path('users/',include('users.urls')),
    # 搜索页面
    path('search/',include('search_info.urls'))
    # path('admin/', admin.site.urls),
]
