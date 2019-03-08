from django.shortcuts import render
from .models import MajorCates,Majors
from user.models import Provinces, Citys
from school.models import Schools
import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from major.pages import Page


# 专业列表
def get_major(request):
    major = Majors.objects.filter(is_status=1)
    # 获取关键字类型
    keyword_name = request.GET.get('keyword_name', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    # 关键词选择
    if keyword_name == 'major':
        if keyword:
            major = major.filter(major_name__contains=keyword)
    elif keyword_name == 'school':
        if keyword:
            major = major.filter(school__name__contains=keyword)
    majors = major
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, major)
    context = {
        'major': pages['data'],
        'majors': majors,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword_name':keyword_name,
        'keyword':keyword
    }

    return render(request,'major/major-list.html',context=context)

# 专业详细信息
def detail_major(request):
    major_id = request.POST.get('major_id')
    major = Majors.objects.get(id=major_id)
    context = {
        'major':major
    }
    return render(request,'major/major-detail.html',context=context)

# 删除专业信息
def delete_major(request):
    major_id = request.GET.get('major_id')
    info = Majors.objects.get(id=major_id)
    info.is_status = 0
    info.save()
    majors = Majors.objects.filter(is_status=1)
    context = {
        'major':majors
    }
    return render(request,'major/major-list.html',context=context)

# 已删除专业列表
def get_del_major(request):
    major = Majors.objects.filter(is_status=0)
    # 获取关键字类型
    keyword_name = request.GET.get('keyword_name', '')
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    # 关键词选择
    if keyword_name == 'major':
        if keyword:
            major = major.filter(major_name__contains=keyword)
    elif keyword_name == 'school':
        if keyword:
            major = major.filter(school__name__contains=keyword)
    majors = major
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, major)
    context = {
        'major': pages['data'],
        'majors': majors,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword_name': keyword_name,
        'keyword': keyword
    }
    return render(request,'major/major-del.html',context=context)

# 恢复专业
def recover_major(request):
    major_id = request.GET.get('major_id')
    major = Majors.objects.get(id=major_id)
    major.is_status = 1
    major.save()
    majors = Majors.objects.filter(is_status=0)
    context = {
        'major':majors
    }
    return render(request,'major/major-del.html',context=context)

# 彻底删除专业
def las_del_major(request):
    major_id = request.GET.get('major_id')
    Majors.objects.filter(id=major_id).delete()
    major = Majors.objects.filter(is_status=0)
    return render(request,'major/major-del.html',context={'major':major})

# 添加专业信息
class  AddMajor(View):
    def get(self,request):
        school = Schools.objects.filter(is_status=1)
        major_cate = MajorCates.objects.filter(is_status=1).exclude(pid=0)
        context = {
            'school':school,
            'major_cate':major_cate
        }
        return render(request,'major/major-add.html',context=context)

    def post(self,request):
        major_name = request.POST.get('major_name')
        times = request.POST.get('times')
        level = request.POST.get('level')
        is_recommend = request.POST.get('is_recommend')
        school = request.POST.get('school')
        major_cate = request.POST.get('cate')
        Majors.objects.filter(major_name=major_name).create(
            major_name=major_name,
            times=times,
            level=level,
            is_recommend=is_recommend,
            school=Schools.objects.get(id=school),
            major_category=MajorCates.objects.get(id=major_cate),
            is_fast=request.POST.get('is_fast'),
            is_special=request.POST.get('is_special')
        )
        return JsonResponse({
            'status':'success',
            'message':'添加成功',
            'info':''
        })


# 编辑专业信息
class EditMajor(View):
    def get(self,request):
        major_id = request.GET.get('major_id')
        major = Majors.objects.get(id=major_id)
        school = Schools.objects.filter(is_status=1)
        major_cate = MajorCates.objects.filter(is_status=1).exclude(pid=0)
        context = {
            'major': major,
            'school': school,
            'major_cate': major_cate
        }
        return render(request,'major/major-edit.html',context=context)

    def post(self,request):
        major_id = request.POST.get('major_id',None)
        school = request.POST.get('school',None)
        major_cate = request.POST.get('cate',None)
        major = Majors.objects.get(id=major_id)
        print(request.FILES.get('major_image',None))
        major.major_image = request.FILES.get('major_image',None)
        major.major_name = request.POST.get('major_name',None)
        major.major_desciption = request.POST.get('desciption',None)
        major.times= request.POST.get('times',None)
        major.count= request.POST.get('count',None)
        major.level= request.POST.get('level',None)
        major.is_recommend= request.POST.get('is_recommend',None)
        major.is_fast= request.POST.get('is_fast',None)
        major.is_special= request.POST.get('is_special',None)
        major.detail= request.POST.get('detail',None)
        major.is_status= request.POST.get('is_status',None)
        major.school = Schools.objects.get(id=school)
        major.major_category = MajorCates.objects.get(id=major_cate)
        major.save()
        return HttpResponse('修改成功')


# 专业分类表
def get_cate(request):
    cate = MajorCates.objects.filter(is_status=1).order_by('id')
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    # 关键词选择
    if keyword:
        cate = cate.filter(catename__contains=keyword)
    cates = cate

    # 从前端获取当前的页码数
    page = request.GET.get('page',1)
    pages = Page.get_page(request,page,cate)
    context = {
        'cate':pages['data'],
        'cates':cates,
        'paginator':pages['paginator'],
        'currentPage':pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'major/cate-list.html',context=context)


# 添加分类
class AddCate(View):
    def get(self,request):
        return render(request,'major/cate-add.html')

    def post(self,request):
        cate_name = request.POST.get('cate_name')
        pid = request.POST.get('pid')
        info = MajorCates.objects.filter(catename=cate_name).exists()
        if info:
            return JsonResponse({
                'status':'fail',
                'message':'分类已存在',
                'tagid':'name',
            })
        else:
            MajorCates.objects.create(
                catename=cate_name,
                pid = pid
            )
            return JsonResponse({
                'status':'success',
                'message':'添加成功',
                'info':''
            })


# 获取大分类
def have_cate(request):
    cate_id = request.GET.get('cate_id',None)
    if cate_id == '0':
        cate = MajorCates.objects.filter(pid=0)
        list = []
        for item in cate.all():
            list.append([item.id,item.catename])
        return JsonResponse({
            'status':'success',
            'data':list
        })
    else:
        return JsonResponse({'status':'fail'})


# 编辑分类
class EditCate(View):
    def get(self,request):
        cate_id = request.GET.get('cate_id')
        cate = MajorCates.objects.get(id=cate_id)
        cates = MajorCates.objects.filter(is_status=1)
        return render(request,'major/cate-edit.html',context={
            'cate':cate,
            'cates':cates
        })

    def post(self,request):
        cate_id = request.POST.get('cate_id')
        print(cate_id)
        pid = request.POST.get('pid')
        print(pid)
        cate = MajorCates.objects.get(id=cate_id)
        cate.pid = pid
        cate.is_status = request.POST.get('is_status')
        cate.save()
        return HttpResponse('修改成功')


# 删除分类
def del_cate(request):
    cate_id = request.GET.get('cate_id')
    cate = MajorCates.objects.get(id=cate_id)
    cate.is_status = 0
    cate.save()
    cates = MajorCates.objects.filter(is_status=1)
    return render(request,'major/cate-list.html',context={'cate':cates})

# 已删除分类
def get_del_cate(request):
    cate = MajorCates.objects.filter(is_status=0)
    cates = MajorCates.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    # 关键词选择
    if keyword:
        cate = cate.filter(catename__contains=keyword)
    cate1 = cate

    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, cate)
    context = {
        'cate': pages['data'],
        'cates': cates,
        'cate1':cate1,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'major/cate-del.html',context=context)

# 恢复
def recover_cate(request):
    cate_id = request.GET.get('cate_id')
    cate = MajorCates.objects.get(id=cate_id)
    cate.is_status = 1
    cate.save()
    cate = MajorCates.objects.filter(is_status=0)
    cates = MajorCates.objects.filter(is_status=1)
    context = {
        'cate': cate,
        'cates':cates
    }
    return render(request, 'major/cate-del.html', context=context)


# 彻底删除
def las_del_cate(request):
    cate_id = request.GET.get('cate_id')
    MajorCates.objects.filter(id=cate_id).delete()
    cate = MajorCates.objects.filter(is_status=0)
    cates = MajorCates.objects.filter(is_status=1)
    context = {
        'cate': cate,
        'cates': cates
    }
    return render(request, 'major/cate-del.html', context=context)
