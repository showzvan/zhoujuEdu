from django.shortcuts import render
from school.models import Schools,SchoolIntro,SchoolType,SchoolFeatures
from user.models import Provinces
from major.models import Majors
from server.models import ServerPosts
from posts.models import Posts
from choose_major.pages import Page


def school(request):
    # 获取学校
    schools = Schools.objects.filter(is_status=1)
    # 获取热门院校
    hot_school = schools.order_by('-count')[:12]
    # 获取报考指南
    hot_posts = ServerPosts.objects.filter(cateid_id=1).order_by('-views')[:5]
    # 获取学校类型
    school_types = SchoolType.objects.filter(is_status=1)
    # 获取院校特征
    school_features = SchoolFeatures.objects.filter(is_status=1)
    # 推荐专业
    recommends = Majors.objects.filter(is_recommend=1)
    # 获取省份
    sch_pro = Schools.objects.values('sch_pro').distinct()
    sch_pro = [int(x['sch_pro']) for x in sch_pro]
    # 获取所有省
    pro = Provinces.objects.all()

    # 获取省份id
    pro_id = request.GET.get('p','')
    if pro_id:
        schools = schools.filter(sch_pro_id=int(pro_id))

    # 获取类型
    type_id = request.GET.get('t', '')
    if type_id:
        schools = schools.filter(school_type__id=int(type_id))

    # 获取特征
    feature_id = request.GET.get('f', '')
    if feature_id:
        schools = schools.filter(scholl_feature__id = int(feature_id))

    # 获取排序
    sort = request.GET.get('sort', '')
    if sort:
        if sort == 'normal':
            schools = schools
        elif sort == 'count':
            schools = schools.order_by('-count')

    # 分页展示
    data = schools
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 20)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'schools':schools,
        'hot_school':hot_school,
        'hot_posts':hot_posts,
        'sch_pro':sch_pro,
        'recommends':recommends,
        'pros':pro,
        'school_types':school_types,
        'school_features':school_features,
        'pro_id':pro_id,
        'type_id':type_id,
        'feature_id':feature_id,
        'sort':sort,
    }
    return render(request,'choose_school/school.html',context=context)

# 招生简章
def school_intro(request,school_id):
    school = Schools.objects.get(id=school_id)
    school_intro = SchoolIntro.objects.all()
    context = {
        'school':school,
        'school_intro':school_intro
    }
    return render(request,'choose_school/school-intro.html',context=context)


def school_detail(request,school_id):
    # 院校信息
    school = Schools.objects.get(id=int(school_id))
    # 推荐专业
    recommends = Majors.objects.filter(is_recommend=1,school_id=school_id)[:4]
    # 开设专业数量
    majors_count = Majors.objects.filter(is_status=1,school_id=school_id).count()
    # 相关地区院校推荐
    pro_school = Schools.objects.filter(is_status=1,sch_pro_id=school.sch_pro_id).exclude(id=school.id)
    # 相同类型院校推荐
    try:
        same_type = Schools.objects.filter(is_status=1,school_type__in=school.school_type.all()).exclude(id=school.id)
    except:
        same_type = []
    # 院校新闻
    try:
        school_news = Posts.objects.order_by('-edit_time').filter(is_status=1,school_id=school.id)[:5]
    except:
        school_news = []
    # 常见问题
    try:
        question_news = Posts.objects.order_by('-views').filter(is_status=1,school_id=school.id)[:5]
    except:
        question_news = []
    # 学院院历
    try:
        yuan_id = Posts.objects.filter(post_title__contains='学院院历',school_id=school_id).order_by('-edit_time').first()
    except:
        yuan_id = []

    # 开设专业
    majors = Majors.objects.filter(is_status=1,school_id=school_id)[:10]
    # 学校类型
    school_type = school.school_type.all()
    # 院校特征
    school_feature = school.scholl_feature.all()
    # 学校层次
    school_level = Majors.objects.filter(school_id=school_id).values('level').distinct().order_by('id')

    context = {
        'school':school,
        'recommends':recommends,
        'majors':majors,
        'school_type':school_type,
        'school_feature':school_feature,
        'school_level':school_level,
        'majors_count':majors_count,
        'pro_school':pro_school,
        'same_type':same_type,
        'school_news':school_news,
        'question_news':question_news,
        'yuan_id':yuan_id
    }
    return render(request,'choose_school/school-detail.html',context=context)


def school_filter(request,pro_code):
    schools = Schools.objects.filter(is_status=1)
    school_types = SchoolType.objects.filter(is_status=1)
    school_features = SchoolFeatures.objects.filter(is_status=1)
    sch_pro = Schools.objects.values('sch_pro').distinct()
    sch_pro = [int(x['sch_pro']) for x in sch_pro]
    pro = Provinces.objects.all()
    print(sch_pro)
    context = {
        'schools': schools,
        'sch_pro': sch_pro,
        'pros': pro,
        'school_types': school_types,
        'school_features': school_features,
    }
    return render(request, 'choose_school/school.html', context=context)
