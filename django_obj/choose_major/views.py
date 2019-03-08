from django.shortcuts import render
from major.models import Majors,MajorCates
from school.models import Schools
from django.db.models import Q
from .pages import Page



def choose_major(request):
    # 获取专业
    majors = Majors.objects.order_by('-count').filter(is_status=1)
    # 获取专业大类
    majorCates = MajorCates.objects.order_by('id').filter(is_status=1,pid=0)
    # 获取专业小类
    majorLittle = MajorCates.objects.order_by('id').filter(is_status=1).exclude(pid=0)
    # 获取学校
    schools = Schools.objects.filter(is_status=1)
    # 获取热门专业
    hot_major = majors[:5]

    # 选择专业大类
    dl_id = request.GET.get('d','')
    if dl_id:
        majors = majors.filter(major_category__pid=int(dl_id))
        majorCates = majorCates.filter(id=int(dl_id))
        majorLittle = majorLittle.filter(pid=int(dl_id))
        schools = schools.filter(majors__major_category__pid=int(dl_id)).distinct()
    # 选择专业小类
    xl_id = request.GET.get('x','')
    if xl_id:
        majors = majors.filter(major_category_id=int(xl_id))
        majorLittle = majorLittle.filter(id=int(xl_id))
        pid = majorLittle.get(id=int(xl_id))
        majorCates = majorCates.filter(id=pid.pid)
        schools = schools.filter(majors__major_category__id=int(xl_id)).distinct()
    # 选择学校
    school_id = request.GET.get('s','')
    if school_id:
        majors = majors.filter(school_id=int(school_id))
        majorLittle = majorLittle.filter(majors__school_id=int(school_id)).distinct()
        majorCates = MajorCates.objects.filter(id__in=majorLittle.values('pid')).distinct()
        schools = schools.filter(id=int(school_id))
    # 选择层次
    level_code = request.GET.get('l','')
    if level_code:
        majors = majors.filter(level=int(level_code))
        majorLittle = majorLittle.filter(majors__level=int(level_code)).distinct().distinct()
        majorCates = MajorCates.objects.filter(id__in=majorLittle.values('pid')).distinct()
        schools = schools.filter(id__in=majors.values('school__id')).distinct()

    # 获取层次
    level = majors.values('level')
    level = sorted(set([x['level'] for x in level]))

    # 录取快的学校
    is_fast = request.GET.get('r','')
    if is_fast:
        if is_fast == '1':
            majors = Majors.objects.order_by('-count').filter(is_fast=1)
    # 只看名校
    type_code = request.GET.get('type','')
    if type_code:
        if type_code == '0':
            majors = majors.filter(Q(school__is_double=1)|Q(school__is_211=1)|Q(school__is_985=1))
        # 可报网络专业
        elif type_code == '1':
            majors = majors.filter(is_net=1)

    # 分页展示
    data = majors
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data':pages['data'],
        'paginator':pages['paginator'],
        'currentPage':pages['currentPage'],
        'page_range':pages['page_range'],
        'majors':majors,
        'majorCates':majorCates,
        'majorLittle':majorLittle,
        'schools':schools,
        'hot_major':hot_major,
        'level':level,
        'dl_id':dl_id,
        'xl_id':xl_id,
        'school_id':school_id,
        'level_code':level_code,
        'is_fast':is_fast,
        'type_code':type_code,
    }
    return render(request,'choose_major/major.html',context=context)



# 专业信息
def major_detail(request,major_pk,school_pk):
    major = Majors.objects.get(pk=major_pk)
    # 获取学校
    school = Schools.objects.get(id=school_pk)
    schools = Schools.objects.distinct().filter(majors__major_name=major.major_name) # 查询并去重
    # 推荐专业
    hot_major = Majors.objects.filter(is_status=1,is_recommend=1,school_id=school_pk)[:5]
    major_level = Majors.objects.filter(major_name=major.major_name).filter(school_id=school_pk)
    context = {
        'major':major,
        'schools':schools,
        'major_level':major_level,
        'school':school,
        'hot_major':hot_major,
    }
    return render(request,'choose_major/major-detail.html',context=context)


# 获取层次
def major_school(request):
    school_id = request.GET.get('school_id')
    major_name = request.GET.get('major_name')
    major = Majors.objects.filter(major_name=major_name).filter(school_id=school_id).first()
    major_level = Majors.objects.filter(major_name=major_name).filter(school_id=school_id)
    school = Schools.objects.get(id=school_id)
    schools = Schools.objects.distinct().filter(majors__major_name=major.major_name)
    context = {
        'major': major,
        'schools': schools,
        'major_level': major_level,
        'school':school
    }
    return render(request, 'choose_major/major-detail.html', context=context)


# 通过层次专业获取学校
def level_school(request):
    level = request.GET.get('level')
    major_name = request.GET.get('major_name')
    major_id = request.GET.get('major_id')
    schools = Schools.objects.distinct().filter(majors__major_name=major_name).filter(majors__level=level)
    major = Majors.objects.get(id=major_id)
    major_level = Majors.objects.filter(major_name=major_name).filter(school_id=major.school_id)
    school = Schools.objects.get(id=major.school_id)
    context = {
        'major': major,
        'schools': schools,
        'major_level': major_level,
        'school':school
    }
    return render(request, 'choose_major/major-detail.html', context=context)

