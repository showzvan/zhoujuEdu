#-*-coding:utf-8-*-
from detail.models import Regions,Links
from enter.forms import RegisterForm
from captcha.views import captcha_image_url
from captcha.fields import CaptchaStore
# 查询公共模板上的数据


def navigation_bar(request):
    # 查询城市信息
    nav_citys = Regions.objects.filter(is_status=1)
    # 查询热门城市
    nav_hot_city = Regions.objects.filter(is_status=1,is_hot=1)
    # 查询友情链接
    nav_links = Links.objects.filter(is_status=1)
    # 查询session信息
    nav_user_phone = request.session.get('user_phone','')
    # 图片验证码
    # hashkey验证码生成的秘钥，image_url验证码的图片地址
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    login_form = RegisterForm()
    return {
        'nav_citys':nav_citys,
        'nav_hot_city':nav_hot_city,
        'nav_links':nav_links,
        'nav_user_phone':nav_user_phone,
        'hashkey':hashkey,
        'image_url':image_url,
        'login_form':login_form
    }