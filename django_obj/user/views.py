from django.shortcuts import render
from .models import Users, Provinces, Citys, Areas, EmailVerifyRecord
from cms.models import Admins
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from cms.check import Base
import json
from utils import email_send
from major.pages import Page


# 用户列表
def indexList(request):
    users = Users.objects.filter(is_status=1)
    # 获取时间类型
    time_type = request.GET.get('time_type', '')
    # 获取开始时间
    start_time = request.GET.get('start_time', '')
    # 获取结束时间
    end_time = request.GET.get('end_time', '')
    # 获取关键字类型
    keyword_name = request.GET.get('keyword_name', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 如果选择的是注册时间
    if time_type == 'reg-time':
        if start_time:
            if end_time:
                users = users.filter(reg_time__range=(start_time, end_time))
            else:
                users = users.filter(reg_time__gte=start_time)
        elif end_time:
            if not start_time:
                users = users.filter(reg_time__lte=end_time)
    # 如果选择的是登录时间
    if time_type == 'login-time':
        if start_time:
            if end_time:
                users = users.filter(last_time__range=(start_time, end_time))
            else:
                users = users.filter(last_time__gte=start_time)
        elif end_time:
            if not start_time:
                users = users.filter(last_time__lte=end_time)
    # 关键词选择
    if keyword_name == 'username':
        if keyword:
            users = users.filter(nickname__contains=keyword)
    elif keyword_name == 'userphone':
        if keyword:
            users = users.filter(phone__contains=keyword)
    else:
        if keyword:
            users = users.filter(email__contains=keyword)

    user = users
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, users)
    context = {
        'users': pages['data'],
        'user': user,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'time_type': time_type,
        'keyword_name': keyword_name
    }
    return render(request, 'user/users-list.html', context=context)


# 添加用户
class AddUserView(View):
    def get(self, request):
        return render(request, 'user/users-add.html')

    def post(self, request):
        nickName = request.POST.get("nickname", None)
        info = Users.objects.filter(nickname=nickName).exists()
        if info:
            return JsonResponse({
                "status": "fail",
                "message": "当前用户已存在",
                "tagid": "nickname"
            })
        # 增加数据
        else:
            Users.objects.create(
                nickname=nickName,
                password=make_password(request.POST.get("password", None)),
                email=request.POST.get("email", None),
                reg_ip=Base.get_ip(request),
                reg_time=Base.getNowTime(request)
            )
            return JsonResponse({
                "status": "success",
                "message": "注册成功",
                "info": "",
            })


def delete_user(request):
    user_id = request.GET.get('user_id')
    Users.objects.filter(id=user_id).update(is_status=0)
    users = Users.objects.filter(is_status=1)
    context = {
        'users': users
    }
    return render(request, 'user/users-list.html', context=context)


def delete_user_list(request):
    users = Users.objects.filter(is_status=0)
    # 获取时间类型
    time_type = request.GET.get('time_type', '')
    # 获取开始时间
    start_time = request.GET.get('start_time', '')
    # 获取结束时间
    end_time = request.GET.get('end_time', '')
    # 获取关键字类型
    keyword_name = request.GET.get('keyword_name', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 如果选择的是注册时间
    if time_type == 'reg-time':
        if start_time:
            if end_time:
                users = users.filter(reg_time__range=(start_time, end_time))
            else:
                users = users.filter(reg_time__gte=start_time)
        elif end_time:
            if not start_time:
                users = users.filter(reg_time__lte=end_time)
    # 如果选择的是登录时间
    if time_type == 'login-time':
        if start_time:
            if end_time:
                users = users.filter(last_time__range=(start_time, end_time))
            else:
                users = users.filter(last_time__gte=start_time)
        elif end_time:
            if not start_time:
                users = users.filter(last_time__lte=end_time)
    # 关键词选择
    if keyword_name == 'username':
        if keyword:
            users = users.filter(nickname__contains=keyword)
    elif keyword_name == 'userphone':
        if keyword:
            users = users.filter(phone__contains=keyword)
    else:
        if keyword:
            users = users.filter(email__contains=keyword)
    user_p = users
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, users)
    context = {
        'users': pages['data'],
        'user_p': user_p,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'time_type': time_type,
        'keyword_name': keyword_name
    }
    return render(request, 'user/delete_user_list.html', context=context)


def recover_user(request):
    user_id = request.GET.get('user_id', None)
    Users.objects.filter(id=user_id).update(is_status=1)
    users = Users.objects.filter(is_status=0)
    context = {
        'users': users
    }
    return render(request, 'user/delete_user_list.html', context=context)


def last_delete_user(request):
    user_id = request.GET.get('user_id', None)
    Users.objects.filter(id=user_id).delete()
    users = Users.objects.filter(is_status=0)
    context = {
        'users': users
    }
    return render(request, 'user/delete_user_list.html', context=context)


# 编辑
class EditUser(View):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        info = Users.objects.filter(id=user_id)
        if info:
            user = Users.objects.get(pk=user_id)
            provinces = Provinces.objects.all()
            context = {
                'users': user,
                'provinces': provinces
            }
            return render(request, 'user/users-edit.html', context=context)


def get_city(request):
    proid = request.POST.get('proid', None)
    info = Citys.objects.filter(provinceid=proid)
    list = []
    for item in info.all():
        list.append([item.cityid, item.city])  # 处理成列表格式
    return JsonResponse({'data': list})


def get_country(request):
    cityid = request.POST.get('cityid', None)
    info = Areas.objects.filter(cityid=cityid)
    list = []
    for item in info.all():
        list.append([item.areaid, item.area])  # 处理成列表格式
    return JsonResponse({'data': list})


# 更改信息
def user_info(request):
    data = request.POST.get('data', None)
    userid = request.POST.get('user_id', None)

    data = json.loads(data)

    users = Users.objects.get(pk=userid)
    if data['province'] != '':
        users.province = Provinces.objects.get(provinceid=data['province'])
        if data['city'] != '':
            users.city = Citys.objects.get(cityid=data['city'])
            if data['country'] != '':
                users.country = Areas.objects.get(areaid=data['country'])

    if data['email'] != '':
        users.email = data['email']

    if data['phone'] != '':
        users.phone = data['phone']

    if data['is_student'] != '':
        users.is_student = data['is_student']

    if data['education']:
        users.education = data['education']

    if data['major']:
        users.major = data['major']

    if data['dgree']:
        users.dgree = data['dgree']

    if data['school']:
        users.school = data['school']

    if data['is_status']:
        users.is_status = data['is_status']

    users.save()

    return JsonResponse({
        "status": "success",
        "message": "用户信息变更成功！",
        "info": ""
    })


# 修改密码
class EditPwd(View):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        users = Users.objects.get(id=user_id)
        if user_id:
            return render(request, 'user/users-chpwd.html', context={'users': users})

    def post(self, request):
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        newPwd = make_password(password=password)
        users = Users.objects.get(id=user_id)
        users.password = newPwd
        users.save()
        return JsonResponse({
            "status": "success",
            "message": "成功",
            "info": ""
        })


def detail_user(request):
    user_id = request.POST.get('user_id', None)
    user = Users.objects.get(id=user_id)
    return render(request, 'user/users-detail.html', context={'user': user})


# 用户头像上传
class UserImageUpload(View):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        user = Users.objects.get(id=user_id)
        return render(request, 'user/users-avatar.html', context={'user': user})

    def post(self, request):
        user_id = request.POST.get('user_id', None)
        user = Users.objects.get(id=user_id)

        user_img = request.FILES.get('avatar')
        try:
            user.user_img = user_img
            user.save()
            data = {'state': 1}
        except:
            data = {'state': 0}
        return JsonResponse(data)


# 邮件重置密码
class RestartPwd(View):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        user = Users.objects.get(id=user_id)
        return render(request, 'user/restart.html', context={'user': user})

    def post(self, request):
        user_id = request.POST.get('user_id', None)
        user = Users.objects.get(id=user_id)
        email = user.email
        email_send.send_register_email(email)
        return HttpResponse(100)


def change_pwd(request, active_code):
    record = EmailVerifyRecord.objects.filter(code=active_code)
    if record:
        for i in record:
            email = i.email
            users = Users.objects.get(email=email)
            if users:
                return render(request, 'user/pwd_reset.html', {'users': users})


# 邮箱重置密码
def resetPwd(request):
    user_id = request.POST.get('user_id', None)
    password = request.POST.get('password', None)
    newPwd = make_password(password=password)
    users = Users.objects.get(id=user_id)
    users.password = newPwd
    users.save()
    return JsonResponse({
        "status": "success",
        "message": "成功",
        "info": ""
    })


# 管理员列表
def admin_list(request):
    ad_user = Admins.objects.filter(is_status=1)
    # 获取时间类型
    time_type = request.GET.get('time_type', '')
    # 获取开始时间
    start_time = request.GET.get('start_time', '')
    # 获取结束时间
    end_time = request.GET.get('end_time', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 如果选择的是注册时间
    if time_type == 'reg-time':
        if start_time:
            if end_time:
                ad_user = ad_user.filter(reg_time__range=(start_time, end_time))
            else:
                ad_user = ad_user.filter(reg_time__gte=start_time)
        elif end_time:
            if not start_time:
                ad_user = ad_user.filter(reg_time__lte=end_time)
    # 如果选择的是登录时间
    if time_type == 'login-time':
        if start_time:
            if end_time:
                ad_user = ad_user.filter(last_time__range=(start_time, end_time))
            else:
                ad_user = ad_user.filter(last_time__gte=start_time)
        elif end_time:
            if not start_time:
                ad_user = ad_user.filter(last_time__lte=end_time)
    # 关键词选择
    if keyword:
        ad_user = ad_user.filter(admin_name__contains=keyword)
    ad_users = ad_user

    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, ad_user)
    context = {
        'ad_user': pages['data'],
        'ad_users': ad_users,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'time_type': time_type,
    }
    return render(request, 'user/admin-list.html', context=context)


# 删除管理员
def delete_admin(request):
    ad_id = request.GET.get('admin_id', None)
    ad_users = Admins.objects.get(id=ad_id)
    ad_users.is_status = 0
    ad_users.save()
    ad_user = Admins.objects.filter(is_status=1)
    return render(request, 'user/admin-list.html', context={'ad_user': ad_user})


# 已删除管理员
def delete_admin_list(request):
    ad_user = Admins.objects.filter(is_status=0)
    # 获取时间类型
    time_type = request.GET.get('time_type', '')
    # 获取开始时间
    start_time = request.GET.get('start_time', '')
    # 获取结束时间
    end_time = request.GET.get('end_time', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 如果选择的是注册时间
    if time_type == 'reg-time':
        if start_time:
            if end_time:
                ad_user = ad_user.filter(reg_time__range=(start_time, end_time))
            else:
                ad_user = ad_user.filter(reg_time__gte=start_time)
        elif end_time:
            if not start_time:
                ad_user = ad_user.filter(reg_time__lte=end_time)
    # 如果选择的是登录时间
    if time_type == 'login-time':
        if start_time:
            if end_time:
                ad_user = ad_user.filter(last_time__range=(start_time, end_time))
            else:
                ad_user = ad_user.filter(last_time__gte=start_time)
        elif end_time:
            if not start_time:
                ad_user = ad_user.filter(last_time__lte=end_time)
    # 关键词选择
    if keyword:
        ad_user = ad_user.filter(admin_name__contains=keyword)
    ad_users = ad_user
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, ad_user)
    context = {
        'ad_user': pages['data'],
        'ad_users': ad_users,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'time_type': time_type,
    }
    return render(request, 'user/delete_admin_list.html', context=context)


# 恢复管理员
def recover_admin(request):
    ad_id = request.GET.get('admin_id', None)
    ad_users = Admins.objects.get(id=ad_id)
    ad_users.is_status = 1
    ad_users.save()
    ad_user = Admins.objects.filter(is_status=0)
    context = {
        'ad_user': ad_user
    }
    return render(request, 'user/delete_admin_list.html', context=context)


# 彻底删除管理员
def last_delete_admin(request):
    ad_id = request.GET.get('admin_id', None)
    Admins.objects.filter(id=ad_id).delete()
    ad_user = Admins.objects.filter(is_status=0)
    context = {
        'ad_user': ad_user
    }
    return render(request, 'user/delete_admin_list.html', context=context)


# 添加管理员
class AddAdmin(View):
    def get(self, request):
        return render(request, 'user/admin-add.html')

    def post(self, request):
        admin_name = request.POST.get('admin_name', None)
        info = Admins.objects.filter(admin_name=admin_name).exists()
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '当前用户已存在',
                'tagid': 'nickname',
            })
        # 增加数据
        else:
            Admins.objects.create(
                admin_name=admin_name,
                password=make_password(request.POST.get("password", None)),
                reg_time=Base.getNowTime(request),
                reg_ip=Base.get_ip(request)
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': ''
            })


class EditAdPwd(View):
    def get(self, request):
        admin_id = request.GET.get('admin_id', None)
        ad_user = Admins.objects.get(id=admin_id)
        return render(request, 'user/admins-chpwd.html', context={'ad_user': ad_user})

    def post(self, request):
        admin_id = request.POST.get('admin_id', None)
        password = request.POST.get('password', None)
        newPwd = make_password(password=password)
        info = Admins.objects.get(id=admin_id)
        info.password = newPwd
        info.save()
        return JsonResponse({
            'status': 'success',
            'message': '密码修改成功',
            'info': ''
        })


# 修改管理员头像
class AdUpload(View):
    def get(self, request):
        admin_id = request.GET.get('admin_id')
        ad_user = Admins.objects.get(id=admin_id)
        return render(request, 'user/admins-avatar.html', context={'ad_user': ad_user})

    def post(self, request):
        admin_id = request.POST.get('admin_id')
        ad_user = Admins.objects.get(id=admin_id)
        ad_img = request.FILES.get('avatar')
        print(ad_img)
        try:
            ad_user.admin_img = ad_img
            ad_user.save()
            data = {
                'state': 1
            }
        except:
            data = {
                'state': 0
            }
        return JsonResponse(data)
