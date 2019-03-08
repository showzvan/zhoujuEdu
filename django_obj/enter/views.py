from django.shortcuts import render
from django.http import JsonResponse
from major.models import Majors
from school.models import Schools
from order.models import Orders
from . forms import RegisterForm
from django.views import View
from alipay import AliPay,ISVAliPay
import os
from django_obj import settings





def enter(request):
    major_id = request.GET.get('m','')
    school_id = request.GET.get('s','')
    # 图片验证码
    register_form = RegisterForm()
    # 查询专业相关信息
    if major_id:
        major = Majors.objects.get(id=int(major_id))
    else:
        major = ''
    context = {
        'major':major,
        'school_id':school_id,
        'register_form':register_form
    }
    return render(request,'enter/enter.html',context=context)



def enterPay(request):
    idCard = request.POST.get('idCard','')
    real_name = request.POST.get('real_name','')
    phone = request.POST.get('phone','')
    major_code = request.POST.get('major_code','')
    major = Majors.objects.get(id=major_code)
    # 创建订单
    has_order = Orders.objects.filter(real_name=real_name,idcard=idCard,phone=phone,majar_id_id=major_code)
    # 如果订单不存在的情况下，创建订单
    if not has_order:
        Orders.objects.create(
            real_name=real_name,
            idcard=idCard,
            phone=phone,
            majar_id_id=major_code,
            school_id_id=major.id,
            user_id_id=1,
            status='wfk'
        )
    context = {
        'major':major,
        'idCard':idCard,
        'real_name':real_name,
        'phone':phone
    }
    return render(request,'enter/enter-pay.html',context=context)


def pay_success(request):
    return render(request,'enter/enter-success.html')



class ORderPay(View):
    """订单支付"""
    def post(self,request):
        app_private_key_string = open(os.path.join(settings.BASE_DIR,'enter/app_private_key.pem')).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR,'alipay_public_key.pem')).read()

        '''订单支付'''
        # 用户是否登录

        # 接收参数

        # 校验参数

        # 业务处理：使用python sdk调用支付宝接口
        alipay = AliPay(
            appid="2016092800616152",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = True,  # 默认False
        )

        # 调用支付接口
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no='2016092800616152',
            total_amount=200,# 支付总金额
            subject="舟炬教育",
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        # 返回应答
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'pay_url':pay_url})