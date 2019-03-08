from django.shortcuts import render
from .models import Schools, SchoolType, SchoolFeatures
from user.models import Provinces, Citys
import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from major.pages import Page


# 院校列表
def get_school(request):
    school = Schools.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    # 关键词选择
    if keyword:
        school = school.filter(name__contains=keyword)
    schools = school
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, school)
    context = {
        'school': pages['data'],
        'schools': schools,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }

    return render(request, 'school/school-list.html', context=context)


# 编辑院校
class EditSchool(View):
    def get(self, request):
        school_id = request.GET.get('school_id')
        school = Schools.objects.get(id=school_id)
        province = Provinces.objects.all()
        sch_features = SchoolFeatures.objects.filter(is_status=1)
        sch_type = SchoolType.objects.filter(is_status=1)
        context = {
            'sch_type': sch_type,
            'sch_features': sch_features,
            'provinces': province,
            'school': school
        }
        return render(request, 'school/school-edit.html', context=context)

    def post(self, request):
        # 接收数据
        sch_id = request.POST.get("sch_id", None)
        sch_pro = request.POST.get("sch_pro", None)
        sch_city = request.POST.get("sch_city", None)

        schools = Schools.objects.get(id=sch_id)
        """处理数据"""
        data = request.POST.get('data', None)
        data = json.loads(data)

        """处理mtm"""
        school_type = data.pop('school_type')
        school_feature = data.pop('school_feature')

        """处理省份和市的数据"""
        if sch_pro != '':
            schools.sch_pro = Provinces.objects.get(provinceid=sch_pro)
        if sch_city != '':
            schools.sch_city = Citys.objects.get(cityid=sch_city)

        """对mtm进行数据存储处理"""
        if school_type != []:
            schools.school_type.clear()
            schools.school_type.add(*school_type)

        if school_feature != []:
            schools.scholl_feature.clear()
            schools.scholl_feature.add(*school_feature)

        """处理图片数据"""
        banner = request.FILES.get("banner")
        emblem = request.FILES.get("emblem")
        diploma = request.FILES.get("diploma")
        degree = request.FILES.get("degree")

        if banner != None:
            schools.banner = banner
        if emblem != None:
            schools.emblem = emblem
        if diploma != None:
            schools.diploma_images = diploma
        if degree != None:
            schools.degree_images = degree

        schools.save()
        """对其他数据进行处理"""
        sch = Schools.objects.filter(id=sch_id)
        sch.update(**data)

        return HttpResponse("修改成功")


# 详细信息
def detail_sch(request):
    sch_id = request.POST.get('sch_id')
    school = Schools.objects.get(id=sch_id)
    context = {
        'school': school
    }
    return render(request, 'school/school-detail.html', context=context)


# d
def delete_sch(request):
    sch_id = request.GET.get('sch_id')
    school = Schools.objects.get(id=sch_id)
    school.is_status = 0
    school.save()
    info = Schools.objects.filter(is_status=1)
    context = {
        'school': info,
        'message': '删除成功',
        'info': '',
    }
    return render(request, 'school/school-list.html', context=context)


# 已删除院校
def get_del_sch(request):
    school = Schools.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    # 关键词选择
    if keyword:
        school = school.filter(name__contains=keyword)
    schools = school
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, school)
    context = {
        'school': pages['data'],
        'schools': schools,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword,
    }
    return render(request, 'school/school_del.html', context=context)


# 恢复院校
def recover_sch(request):
    sch_id = request.GET.get('sch_id')
    school = Schools.objects.get(id=sch_id)
    school.is_status = 1
    school.save()
    info = Schools.objects.filter(is_status=0)
    context = {
        'school': info
    }
    return render(request, 'school/school_del.html', context=context)


# 彻底删除院校
def las_del_sch(request):
    sch_id = request.GET.get('sch_id')
    Schools.objects.filter(id=sch_id).delete()
    school = Schools.objects.filter(is_status=0)
    return render(request, 'school/school_del.html', context={'school': school})


# 添加院校
class AddSchool(View):
    def get(self, request):
        return render(request, 'school/school-add.html')

    def post(self, request):
        sch_name = request.POST.get('sch_name', None)
        motto = request.POST.get('motto', None)
        is_985 = request.POST.get('is_985', None)
        is_211 = request.POST.get('is_211', None)
        is_double = request.POST.get('is_double', None)
        info = Schools.objects.filter(name=sch_name).exists()
        if info:
            return JsonResponse({
                "status": "fail",
                "message": "当前院校已存在",
                "tagid": "name",
            })
        else:
            Schools.objects.create(
                name=sch_name,
                motto=motto,
                is_985=is_985,
                is_211=is_211,
                is_double=is_double
            )
            return JsonResponse({
                "status": "success",
                "message": "添加成功",
                "info": "",
            })


# 院校类型
def get_type(request):
    type = SchoolType.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 关键词选择
    if keyword:
        type = type.filter(type_name__contains=keyword)
    types = type
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, type)
    context = {
        'types': pages['data'],
        'type': types,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'school/school-type.html', context=context)


# 添加类型
class AddType(View):
    def get(self, request):
        return render(request, 'school/add_type.html')

    def post(self, request):
        name = request.POST.get('type_name')
        notes = request.POST.get('notes')
        info = SchoolType.objects.filter(type_name=name).exists()
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '类型已存在',
                'tagid': 'name',
            })
        else:
            SchoolType.objects.create(
                type_name=name,
                notes=notes
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': ''
            })


# 删除类型
def del_type(request):
    type_id = request.GET.get('type_id')
    type = SchoolType.objects.get(id=type_id)
    type.is_status = 0
    type.save()
    type = SchoolType.objects.filter(is_status=1)
    return render(request, 'school/school-type.html', context={'type': type})


# 已删除院校类型列表
def get_del_type(request):
    type = SchoolType.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 关键词选择
    if keyword:
        type = type.filter(type_name__contains=keyword)
    types = type
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, type)
    context = {
        'types': pages['data'],
        'type': types,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'school/del_type.html', context=context)


# 恢复类型
def recover_type(request):
    typ_id = request.GET.get('typ_id')
    type = SchoolType.objects.get(id=typ_id)
    type.is_status = 1
    type.save()
    types = SchoolType.objects.filter(is_status=0)
    return render(request, 'school/del_type.html', context={'type': types})


# 彻底删除类型
def las_del_type(request):
    type_id = request.GET.get('type_id')
    SchoolType.objects.filter(id=type_id).delete()
    types = SchoolType.objects.filter(is_status=0)
    return render(request, 'school/del_type.html', context={'type': types})


# 编辑类型
class EditType(View):
    def get(self, request):
        type_id = request.GET.get('type_id')
        type = SchoolType.objects.get(id=type_id)
        context = {
            'type': type
        }
        return render(request, 'school/edit_type.html', context=context)

    def post(self, request):
        type_id = request.POST.get('type_id')
        name = request.POST.get('type_name')
        notes = request.POST.get('notes')
        info = SchoolType.objects.get(id=type_id)
        info.notes = notes
        info.is_status = request.POST.get('is_status')
        info.save()
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 院校特征
def get_feature(request):
    feature = SchoolFeatures.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 关键词选择
    if keyword:
        feature = feature.filter(feature_name__contains=keyword)
    features = feature
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, feature)
    context = {
        'data': pages['data'],
        'feature': features,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'school/school-feature.html', context=context)


# 添加院校特性
class AddFeature(View):
    def get(self, request):
        return render(request, 'school/add_feature.html')

    def post(self, request):
        name = request.POST.get('feature_name')
        notes = request.POST.get('notes')
        info = SchoolFeatures.objects.filter(feature_name=name).exists()
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '特性已存在',
                'tagid': 'name',
            })
        else:
            SchoolFeatures.objects.create(
                feature_name=name,
                notes=notes
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': ''
            })


# 编辑院校特性
class EditFeature(View):
    def get(self, request):
        feature_id = request.GET.get('feature_id')

        feature = SchoolFeatures.objects.get(id=feature_id)
        context = {
            'feature': feature
        }
        return render(request, 'school/edit_feature.html', context=context)

    def post(self, request):
        feature_id = request.POST.get('feature_id')
        name = request.POST.get('feature_name')
        notes = request.POST.get('notes')
        info = SchoolFeatures.objects.get(id=feature_id)
        info.notes = notes
        info.is_status = request.POST.get('is_status')
        info.save()
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 删除特性
def delete_feature(request):
    feature_id = request.GET.get('feature_id')
    feature = SchoolFeatures.objects.get(id=feature_id)
    feature.is_status = 0
    feature.save()
    feature = SchoolFeatures.objects.filter(is_status=1)
    return render(request, 'school/school-feature.html', context={'feature': feature})


# 已删除特性列表
def get_del_feature(request):
    feature = SchoolFeatures.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')
    # 关键词选择
    if keyword:
        feature = feature.filter(feature_name__contains=keyword)
    features = feature
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, feature)
    context = {
        'data': pages['data'],
        'feature': features,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'school/del_feature.html', context=context)

# 恢复特性
def recover_feature(request):
    feature_id = request.GET.get('feature_id')
    feature = SchoolFeatures.objects.get(id=feature_id)
    feature.is_status = 1
    feature.save()
    features = SchoolFeatures.objects.filter(is_status=0)
    return render(request, 'school/del_feature.html', context={'feature': features})

# 彻底删除特性
def las_del_feature(request):
    feature_id = request.GET.get('feature_id')
    SchoolFeatures.objects.filter(id=feature_id).delete()
    features = SchoolFeatures.objects.filter(is_status=0)
    return render(request, 'school/del_feature.html', context={'feature': features})