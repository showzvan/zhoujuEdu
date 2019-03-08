from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from cms.check import Base
from . models import Admins
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.
class IndexView(Base):
    def get(self,request):
        # 判断是或否登录
        status = Base.checkUserLogin(request)
        # 已经登录的情况
        if status:
            ad_name = request.session.get('admin_name')
            ad_user = Admins.objects.get(admin_name=ad_name)
            # 获取时间和ip
            ip = Base.get_ip(request)
            NowTime = Base.getNowTime(request)
            # 从传递信息给前台
            context = {
                "ip":ip,
                "info_time":NowTime,
                'ad_user':ad_user
            }
            return render(request,'cms/index.html',context=context)
        else:
            return render(request,'cms/login.html')

    def post(self,request):
        pass


# 登录
class LoginView(Base):
    def get(self,request):
        # 检查登录状态
        login_status = Base.checkUserLogin(request)
        if login_status:
            return render(request,'cms/index.html')
        else:
            return render(request,'cms/login.html')

    def post(self,request):
        # 接收输入信息
        check_name = request.POST.get('admin_name',None)
        check_pwd = request.POST.get('password',None)
        # 验证信息
        check_status = Base.check_data(check_name,check_pwd)
        # 判断当前用户是存在
        info = Admins.objects.filter(admin_name=check_name).exists()
        # 存在
        if info and check_status['errors'] is None:

            pwd = Admins.objects.get(admin_name=check_name).password
            if check_password(check_pwd,pwd):
                # 获取信息
                ip = Base.get_ip(request)
                info = Admins.objects.get(admin_name=check_name)
                info.last_ip = ip
                info.save()
                request.session['admin_name'] = check_name
                # request.session.set_expiry(60)
                request.session.set_expiry(604800)
                info_url = '/cms/'
                return JsonResponse({
                    'status':'success',
                    'message':'登录成功，可以进入首页',
                    'info':info_url
                })
            else:
                return JsonResponse({
                    'status':'fail',
                    'message':'登录失败，密码错误',
                    'info':"请重新输入密码"
                })
        elif info == False:
            return JsonResponse({
                'status': 'fail',
                'message': '当前用户不存在',
                'info': '请检查用户名'
            })
        elif check_status['errors'] is not None:
            return JsonResponse({
                'status': 'fail',
                'message': '登录信息错误',
                'info': check_status['errors']
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'message': '出现未知错误，请重新输入',
                'info': ''
            })


def logout(request):
    request.session.delete()
    return render(request,'cms/login.html')

