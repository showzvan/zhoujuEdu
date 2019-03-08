from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from order.models import Orders
from django.views import View
from school.models import Schools
from major.models import Majors
from user.models import Users
from major.pages import Page


# 报名信息
def order_list(request):
    order = Orders.objects.filter(is_status=1)
    # 获取关键字类型
    keyword_name = request.GET.get('keyword_name', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 关键词选择
    if keyword_name == 'username':
        if keyword:
            order = order.filter(user_id__nickname__contains=keyword)
    elif keyword_name == 'realname':
        if keyword:
            order = order.filter(real_name__contains=keyword)
    else:
        if keyword:
            order = order.filter(phone__contains=keyword)
    orders = order
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, order)
    context = {
        'order': pages['data'],
        'orders': orders,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword_name':keyword_name,
        'keyword':keyword
    }
    return render(request, 'order/order-list.html', context=context)


# 删除订单
def delete_order(request):
    order_id = request.GET.get('order_id')
    order = Orders.objects.get(id=order_id)
    order.is_status = 0
    order.save()
    orders = Orders.objects.filter(is_status=1)
    return render(request, 'order/order-list.html', context={'order': orders})


# 已删除报名信息
def get_del(request):
    order = Orders.objects.filter(is_status=0)
    # 获取关键字类型
    keyword_name = request.GET.get('keyword_name', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 关键词选择
    if keyword_name == 'username':
        if keyword:
            order = order.filter(user_id__nickname__contains=keyword)
    elif keyword_name == 'realname':
        if keyword:
            order = order.filter(real_name__contains=keyword)
    else:
        if keyword:
            order = order.filter(phone__contains=keyword)
    orders = order
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, order)
    context = {
        'order': pages['data'],
        'orders': orders,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword_name':keyword_name,
        'keyword':keyword
    }
    return render(request, 'order/order-del.html', context=context)


# 恢复订单
def re_order(request):
    order_id = request.GET.get('order_id')
    order = Orders.objects.get(id=order_id)
    order.is_status = 1
    order.save()
    orders = Orders.objects.filter(is_status=0)
    return render(request, 'order/order-del.html', context={'order': orders})


# 彻底删除订单
def las_del_order(request):
    order_id = request.GET.get('order_id')
    Orders.objects.get(id=order_id).delete()
    order = Orders.objects.filter(is_status=0)
    context = {
        'order': order
    }
    return render(request, 'order/order-del.html', context=context)


# 订单详情
def detail_order(request):
    order_id = request.POST.get('order_id')
    order = Orders.objects.get(id=order_id)
    context = {
        'order': order
    }
    return render(request, 'order/order-detail.html', context=context)


# 添加新订单
class AddOrder(View):
    def get(self, request):
        school = Schools.objects.filter(is_status=1)
        context = {
            'school': school
        }
        return render(request, 'order/order-add.html', context=context)

    def post(self, request):
        nick_name = request.POST.get('nick_name')
        info = Users.objects.filter(nickname=nick_name).exists()
        if not info:
            return JsonResponse({
                'status': 'fail',
                'message': '用户不存在',
                'tagid': 'name',
            })
        else:
            Orders.objects.create(
                real_name=request.POST.get('name'),
                idcard=request.POST.get('id_card'),
                phone=request.POST.get('phone'),
                status=request.POST.get('status'),
                majar_id_id=request.POST.get('major'),
                user_id=Users.objects.get(nickname=nick_name),
                school_id_id=request.POST.get('school'),
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': '',
            })


# 获取专业信息
def have_major(request):
    school_id = request.GET.get('school_id')
    major = Schools.objects.get(id=school_id).majors_set.all()
    list = []
    for item in major.all():
        list.append([item.id, item.major_name])
    return JsonResponse({
        'status': 'success',
        'data': list
    })


# 编辑订单信息
class EditOrder(View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        order = Orders.objects.get(id=order_id)
        school = Schools.objects.filter(is_status=1)
        context = {
            'order': order,
            'school': school
        }
        return render(request, 'order/order-edit.html', context=context)

    def post(self, request):
        nick_name = request.POST.get('nick_name')
        order_id = request.POST.get('order_id')
        Orders.objects.filter(id=order_id).update(
            real_name=request.POST.get('name'),
            idcard=request.POST.get('id_card'),
            phone=request.POST.get('phone'),
            status=request.POST.get('status'),
            majar_id_id=request.POST.get('major'),
            user_id=Users.objects.get(nickname=nick_name),
            school_id_id=request.POST.get('school'),
        )
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': '',
        })
