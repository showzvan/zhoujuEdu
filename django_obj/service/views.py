from django.shortcuts import render
from django.http import JsonResponse
from server.models import ServerPosts,ServerCategorys
from school.models import Schools
from major.models import Majors
from choose_major.pages import Page
from django.views import View
from order.models import Orders
from server.models import Centers,AQuestions
from user.models import Provinces
from django.db.models import Q


# 服务大厅主页
def service(request):
    cates = ServerCategorys.objects.filter(is_status=1)
    context = {
        'cates':cates
    }
    return render(request,'service/services.html',context=context)


# 文章详情
def post_detail(request,service_id):
    # 获取文章
    post = ServerPosts.objects.get(id=service_id)
    # 获取上一篇文章
    pre_post = ServerPosts.objects.filter(is_status=1).filter(id__gt=service_id).order_by('id')
    if pre_post.count() > 0:
        pre_post = pre_post[0]
    else:
        pre_post = None
    # 获取下一篇文章
    next_post = ServerPosts.objects.filter(is_status=1).filter(id__lt=service_id).order_by('-id')
    if next_post.count() > 0:
        next_post = next_post[0]
    else:
        next_post = None

    # 阅读人数加1
    post.views = int(post.views) + 1
    post.save()
    context = {
        'post':post,
        'pre_post':pre_post,
        'next_post':next_post,
    }
    return render(request,'service/services-posts-detail.html',context=context)


# 报名
def sign(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=1).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts':posts,
        'hot_posts':hot_posts,
        'hot_schools':hot_schools,
        'hot_majors':hot_majors
    }
    return render(request,'service/services-sign-posts.html',context=context)

# 新生入学
def new_exam(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=2).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request, 'service/services-new_exam-posts.html',context=context)

# 专业考试
def exam(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=4).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request, 'service/services-exam-posts.html',context=context)

# 毕业问答
def graduation(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=5).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request, 'service/services-graduation-posts.html',context=context)

# 学生平台使用帮助
def help(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=3).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request,'service/services-posts.html',context=context)


# 报名凭证查询
class Feecard(View):
    def get(self,request):
        return render(request,'service/services-feecard.html')

    def post(self,request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        id_card = request.POST.get('card')
        # 查询相关信息
        order = Orders.objects.filter(Q(real_name=name),Q(phone=phone),Q(idcard=id_card))
        # 分页展示
        data = order
        page = request.GET.get('page', 1)
        pages = Page.get_page(request, page, data, 10)

        context = {
            'data': pages['data'],
            'paginator': pages['paginator'],
            'currentPage': pages['currentPage'],
            'page_range': pages['page_range'],
            'order':order,
            'name':name,
            'phone':phone,
            'id_card':id_card
        }
        return render(request,'service/services-feecard-search.html',context=context)


# 学习中心查询
class Center(View):
    def get(self,request):
        return render(request,'service/services-centerauth.html')

    def post(self,request):
        pass

# 学习中心查询
class CenterSearch(View):
    def get(self,request):
        name = request.GET.get('name')
        # 查询学习中中心, 使用contains 进行模糊查询
        centers = Centers.objects.filter(name__contains=name)
        # 分页展示
        data = centers
        page = request.GET.get('page', 1)
        pages = Page.get_page(request, page, data, 3)

        context = {
            'data': pages['data'],
            'paginator': pages['paginator'],
            'currentPage': pages['currentPage'],
            'page_range': pages['page_range'],
            'name': name,
            'centers': centers
        }
        return render(request, 'service/services-centerauth-search.html', context=context)


# 高校授权查询
class Collegeautho(View):
    def get(self,request):
        schools = Schools.objects.filter(is_status=1)
        context = {
            'schools':schools
        }
        return render(request,'service/services-collegeautho.html',context=context)


# 高校授权查询结果页
def CollegeauthoSearch(request):
    scool_code = request.GET.get('school_code')
    school_name = request.GET.get('school_name')
    centers = Centers.objects.filter(school_id=int(scool_code))
    pro_code = request.GET.get('province_code','')
    # 查询省份
    provinces = Provinces.objects.filter(id__in=centers.values('provinces'))
    if pro_code:
        centers = centers.filter(provinces_id=int(pro_code))
    # 学习中心数量
    center_num = centers.count()

    # 分页展示
    data = centers
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 20)
    # 当前页数据条数
    data_num = len(pages['data'].object_list)
    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'school_code':scool_code,
        'school_name':school_name,
        'centers':centers,
        'center_num':center_num,
        'provinces':provinces,
        'province_code':pro_code,
        'data_num':data_num
    }
    return render(request,'service/services-collegeautho-search.html',context=context)


# 入学测试模拟题下载
class Examdownload(View):
    def get(self,request):
        school_code = request.GET.get('u')
        majors = []
        if school_code:
            schools = Schools.objects.filter(id=int(school_code))
            majors = Majors.objects.filter(school_id=school_code)
        else:
            schools = Schools.objects.filter(is_status=1)
        context = {
            'schools':schools,
            'majors':majors,
        }
        return render(request,'service/services-examdownload.html',context=context)

    def post(self,request):
        school_id = request.POST.get('school_code')
        major_id = request.POST.get('major_id_oes')
        level = request.POST.get('level_id_oes')
        aquestion = AQuestions.objects.filter(school_id=school_id,major_cate_id=major_id,leval=level)
        aquestion_list = []
        for item in aquestion:
            aquestion_list.append([item.school_id.name,item.get_leval_display(),item.name,item.filename.name])
        return JsonResponse({
            'status':'success',
            'count':len(aquestion_list),
            'data':aquestion_list
        })


# 获取专业
def get_major(request):
    school_code = request.POST.get('school_code')
    major = Majors.objects.filter(school_id=school_code)
    major_list = []
    for item in major.all():
        major_list.append([item.id,item.major_name])
    return JsonResponse({'data':major_list})


# 获取层次
def get_level(request):
    school_code = request.POST.get('school_code')
    major_code = request.POST.get('major_id_oes')
    major_name = Majors.objects.get(id=major_code)
    level = Majors.objects.filter(major_name=major_name.major_name,school_id=school_code)
    list = []
    for item in level.all():
        list.append([item.level,item.get_level_display()]) # 获取层次以及层次的显示
    return JsonResponse({'data': list})


# 课件播放器下载
def courseware(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=12).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request,'service/services-courseware-posts.html',context=context)


# 常见校园表格下载
def sch_form(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=13).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request,'service/services-sch_form-posts.html',context=context)


# 常见申请表格下载
def application(request):
    # 获取文章
    posts = ServerPosts.objects.filter(cateid_id=14).filter(is_status=1).order_by('-id')
    # 获取热门文章
    hot_posts = ServerPosts.objects.filter(is_status=1).order_by('-views')[:10]
    # 获取热门院校
    hot_schools = Schools.objects.filter(is_status=1).order_by('-count')[:12]
    # 获取热门专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)

    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts': posts,
        'hot_posts': hot_posts,
        'hot_schools': hot_schools,
        'hot_majors': hot_majors
    }
    return render(request,'service/services-application-posts.html',context=context)
