from django.shortcuts import render

from .models import Links,Regions
from django.views import View
from django.http import JsonResponse,HttpResponse
from major.pages import Page


# 友情链接
def inner_link(request):
    links = Links.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        links = links.filter(link_title__contains=keyword)
    link = links
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, links)
    context = {
        'data': pages['data'],
        'links': link,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'detail/inner_link.html',context=context)


# 添加友情链接
class AddLink(View):
    def get(self,request):
        return render(request,'detail/add_link.html')

    def post(self,request):
        name = request.POST.get('name')
        link = request.POST.get('link')
        if name == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入名称',
                'tagid': 'name'
            })
        if link == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入链接地址',
                'tagid': 'link'
            })
        info = Links.objects.filter(link_title=name).exists()
        if info:
            return JsonResponse({
                'status':'fail',
                'message':'该友情链接已存在',
                'tagid':'name'
            })
        Links.objects.create(
            link_title=name,
            url=link
        )
        return JsonResponse({
            'status': 'success',
            'message': '添加成功',
            'info': ''
        })


# 编辑友情链接
class EditLink(View):
    def get(self,request):
        link_id = request.GET.get('link_id')
        link = Links.objects.get(id=link_id)
        context = {
            'link':link
        }
        return render(request,'detail/edit_link.html',context=context)

    def post(self,request):
        link_id = request.POST.get('link_id')
        name = request.POST.get('name')
        link = request.POST.get('link')
        is_status = request.POST.get('is_status')
        if name == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入名称',
                'tagid': 'name'
            })
        if link == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入链接地址',
                'tagid': 'link'
            })
        info = Links.objects.exclude(id=link_id).filter(link_title=name).exists()
        if info:
            return JsonResponse({
                'status':'fail',
                'message':'该友情链接已存在',
                'tagid':'name'
            })
        links = Links.objects.get(id=link_id)
        links.link_title=name
        links.url=link
        links.is_status = is_status
        links.save()

        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 删除友情链接
def del_link(request):
    link_id = request.GET.get('link_id')
    info = Links.objects.get(id=link_id)
    info.is_status = 0
    info.save()
    links = Links.objects.filter(is_status=1)
    context = {
        'links': links
    }
    return render(request, 'detail/inner_link.html', context=context)


# 已删除友情链接
def get_del_links(request):
    links = Links.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        links = links.filter(link_title__contains=keyword)
    link = links
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, links)
    context = {
        'data': pages['data'],
        'links': link,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'detail/del_inner_link.html', context=context)


# 恢复友情链接
def recover_link(request):
    link_id = request.GET.get('link_id')
    link = Links.objects.get(id=link_id)
    link.is_status = 1
    link.save()
    links = Links.objects.filter(is_status=0)
    context = {
        'links': links
    }
    return render(request, 'detail/del_inner_link.html', context=context)


# 彻底删除友情链接
def las_del_link(request):
    link_id = request.GET.get('link_id')
    Links.objects.get(id=link_id).delete()
    links = Links.objects.filter(is_status=0)
    context = {
        'links': links
    }
    return render(request, 'detail/del_inner_link.html', context=context)


# 城市信息
def get_regions(request):
    regions = Regions.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        regions = regions.filter(cityname__contains=keyword)
    region = regions
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, regions)
    context = {
        'data': pages['data'],
        'regions': region,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'detail/regions_list.html',context=context)


# 添加城市信息
class AddRegion(View):
    def get(self,request):
        return render(request,'detail/add_region.html')

    def post(self,request):
        city_name = request.POST.get('name')
        initials = request.POST.get('initials')
        is_hot = request.POST.get('is_hot')
        info = Regions.objects.filter(cityname=city_name).exists()
        if city_name == '':
            return JsonResponse({
                'status':'fail',
                'message':'请输入城市名称',
                'tagid':'name'
            })
        if initials == '':
            return JsonResponse({
                'status':'fail',
                'message':'请输入首字母',
                'tagid':'initials'
            })
        if info:
            return JsonResponse({
                'status':'fail',
                'message':'城市已存在',
                'tagid':'name'
            })
        Regions.objects.create(
            cityname=city_name,
            initials=initials,
            is_hot=is_hot
        )
        return JsonResponse({
            'status':'success',
            'message':'添加成功',
            'info':''
        })


# 编辑城市信息
class EditRegion(View):
    def get(self,request):
        city_id = request.GET.get('city_id')
        info = Regions.objects.get(id=city_id)
        context = {
            'region':info
        }
        return render(request,'detail/edit_region.html',context=context)

    def post(self,request):
        city_id = request.POST.get('city_id')
        city_name = request.POST.get('name')
        initials = request.POST.get('initials')
        is_hot = request.POST.get('is_hot')
        is_status = request.POST.get('is_status')
        info = Regions.objects.exclude(id=city_id).filter(cityname=city_name).exists()
        if city_name == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入城市名称',
                'tagid': 'name'
            })
        if initials == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入首字母',
                'tagid': 'initials'
            })
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '城市已存在',
                'tagid': 'name'
            })
        region = Regions.objects.get(id=city_id)
        region.cityname=city_name
        region.initials=initials
        region.is_hot=is_hot
        region.is_status=is_status
        region.save()

        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 删除城市
def del_region(request):
    city_id = request.GET.get('city_id')
    info = Regions.objects.get(id=city_id)
    info.is_status = 0
    info.save()
    regions = Regions.objects.filter(is_status=1)
    context = {
        'regions': regions
    }
    return render(request, 'detail/regions_list.html', context=context)


# 已删除城市信息
def get_del_regions(request):
    regions = Regions.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        regions = regions.filter(cityname__contains=keyword)
    region = regions
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, regions)
    context = {
        'data': pages['data'],
        'regions': region,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'detail/del_regions.html',context=context)


# 恢复城市信息
def recover_region(request):
    city_id = request.GET.get('city_id')
    city = Regions.objects.get(id=city_id)
    city.is_status = 1
    city.save()
    regions = Regions.objects.filter(is_status=0)
    context = {
        'regions': regions
    }
    return render(request, 'detail/del_regions.html', context=context)


# 彻底删除城市
def las_del_region(request):
    city_id = request.GET.get('region_id')
    Regions.objects.get(id=city_id).delete()
    regions = Regions.objects.filter(is_status=0)
    context = {
        'regions': regions
    }
    return render(request, 'detail/del_regions.html', context=context)