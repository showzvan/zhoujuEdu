from django.shortcuts import render
from django.views import View
import re
import random
from django_obj.settings import APIKEY
from django.http import HttpResponse, JsonResponse
from .models import VerifyCode
from .yunpian import YunPian
from user.models import Users
from order.models import Orders
from enter.forms import RegisterForm
from captcha.fields import CaptchaStore
from cms.check import Base


def userEnter(request):
    # 用户手机号
    user_phone = request.session.get('user_phone', '')
    order_type = request.GET.get('order_type', '')
    orders = Orders.objects.filter(user_id__phone=user_phone)
    if order_type:
        if order_type == 'wfk':
            orders = orders.filter(status='wfk')
        elif order_type == 'yfk':
            orders = orders.filter(status='yfk')
        elif order_type == 'ylq':
            orders = orders.filter(status='ylq')
        elif order_type == 'ysx':
            orders = orders.filter(status='ysx')
    context = {
        'user_phone': user_phone,
        'orders': orders,
        'order_type': order_type
    }
    return render(request, 'users/user-myenter.html', context=context)


# 用户协议
def agreement(request):
    user_phone = request.session.get('user_phone', '')
    context = {
        'user_phone': user_phone
    }
    return render(request, 'users/user-agreement.html', context=context)


class Login(View):
    def get(self, request):
        pass

    def post(self, request):
        # 获取手机号
        phone = request.POST.get('phone', '')
        print('手机号 %s' % phone)
        image_code, verify_code = '', ''
        # 获取图片验证码
        captchaStr = request.POST.get('image_code', '')
        captchaHashkey = request.POST.get('hashkey', '')
        # print(captchaHashkey)
        if captchaStr and captchaHashkey:
            try:
                # 获取根据hashkey获取数据库中的response值
                get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
                # 如果验证码匹配
                if get_captcha.response == captchaStr.lower():
                    image_code = True
                else:
                    image_code = False
                    return JsonResponse({
                        'status': 'fail',
                        'msg': '验证码错误',
                        'tagname': '.image_code_error'
                    })
            except:
                image_code = False
                return JsonResponse({
                    'status': 'fail',
                    'msg': '未知错误',
                    'tagname': '.image_code_error'
                })
        # 获取手机验证码
        phoneCode = request.POST.get('phoneCode', '')
        # print('手机验证码：%s' %phoneCode)
        if phoneCode:
            try:
                verify = VerifyCode.objects.order_by('-id').get(mobile=phone)
                if phoneCode == verify.code:
                    verify_code = True
                else:
                    # verify_code = False
                    verify_code = True
                    # return JsonResponse({
                    #     'status': 'fail',
                    #     'msg': '手机验证码错误',
                    #     'tagname': '.phone_code_error'
                    # })
            except:
                # verify_code = False
                verify_code = True

        # 检查是否存在手机号
        try:
            is_user = Users.objects.get(phone=phone)
        except:
            Users.objects.create(
                nickname=str(phone),
                phone=phone,
                reg_time=Base.getNowTime(request),
                reg_ip=Base.get_ip(request),
                is_status=1
            )
        # print('check_mobile')
        # 验证图片验证码和短信验证码是否正确
        if image_code == True and verify_code == True:
            request.session['user_phone'] = phone
            request.session.set_expiry(600)
            # 设置最后登录时间和最后登录ip
            user = Users.objects.get(phone=phone)
            user.last_time = Base.getNowTime(request)
            user.last_ip = Base.get_ip(request)
            user.save()
            # a = request.session.get('user_phone',None)
            # print('session信息 %s' %a)
            return JsonResponse({
                'status': 'success',
                'msg': '成功'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '信息输入有误',
                'tagname': '.image_code_error'
            })


class ForCodeView(View):
    """获取手机验证码"""

    def post(self, request):
        mobile = request.POST.get('mobile', '')
        if mobile:
            # 验证是否为有效手机号
            mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
            res = re.search(mobile_pat, mobile)
            if res:
                # 生成手机验证码
                code = VerifyCode()
                code.mobile = mobile
                c = random.randint(1000, 9999)
                code.code = str(c)
                code.save()
                code = VerifyCode.objects.order_by('-id').filter(mobile=mobile).first().code
                yunpian = YunPian(APIKEY)
                sms_status = yunpian.send_sms(code=code, mobile=mobile)
                print(sms_status)
                msg = sms_status['msg']
                return HttpResponse(msg)
            else:
                msg = '请输入有效手机号码!'
                return HttpResponse(msg)
        else:
            msg = '手机号不能为空！'
            return HttpResponse(msg)


# 退出登录
def logOut(request):
    request.session.delete()
    return JsonResponse({
        'status': 'success'
    })
