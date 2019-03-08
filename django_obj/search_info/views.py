from django.shortcuts import render
from school.models import Schools
from major.models import Majors
from server.models import Centers
from posts.models import Posts
from choose_major.pages import Page


def search(request):
    # 关键字
    keyWord = request.GET.get('search','')
    school_info,major_info,center_info,posts_info,all_count,recommends = '','','','','',''
    if keyWord:
        school_info = Schools.objects.filter(name__contains=keyWord)
        major_info = Majors.objects.filter(school__name__contains=keyWord)
        center_info = Centers.objects.filter(name__contains=keyWord)
        posts_info = Posts.objects.filter(post_title__contains=keyWord)
        recommends = Majors.objects.filter(is_recommend=1)
        all_count = school_info.count() + major_info.count() + center_info.count() + posts_info.count()
    context = {
        'keyword':keyWord,
        'school_info':school_info,
        'major_info':major_info,
        'center_info':center_info,
        'posts_info':posts_info,
        'all_count':all_count,
        'recommends':recommends
    }
    return render(request,'search_info/search.html',context=context)


# 搜素学校
def searchSchool(request):
    keyWord = request.GET.get('search', '')
    school_info, major_info, center_info, posts_info, all_count, recommends = '', '', '', '', '', ''
    if keyWord:
        school_info = Schools.objects.filter(name__contains=keyWord)
        major_info = Majors.objects.filter(school__name__contains=keyWord)
        center_info = Centers.objects.filter(name__contains=keyWord)
        posts_info = Posts.objects.filter(post_title__contains=keyWord)
        recommends = Majors.objects.filter(is_recommend=1)
        all_count = school_info.count() + major_info.count() + center_info.count() + posts_info.count()
    # 分页展示
    data = school_info
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)
    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyWord,
        'school_info': school_info,
        'major_info': major_info,
        'center_info': center_info,
        'posts_info': posts_info,
        'all_count': all_count,
        'recommends': recommends
    }
    return render(request, 'search_info/school_info.html', context=context)

# 搜索专业
def searchMajor(request):
    keyWord = request.GET.get('search', '')
    school_info, major_info, center_info, posts_info, all_count, recommends = '', '', '', '', '', ''
    if keyWord:
        school_info = Schools.objects.filter(name__contains=keyWord)
        major_info = Majors.objects.filter(school__name__contains=keyWord)
        center_info = Centers.objects.filter(name__contains=keyWord)
        posts_info = Posts.objects.filter(post_title__contains=keyWord)
        recommends = Majors.objects.filter(is_recommend=1)
        all_count = school_info.count() + major_info.count() + center_info.count() + posts_info.count()

    # 分页展示
    data = major_info
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)
    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyWord,
        'school_info': school_info,
        'major_info': major_info,
        'center_info': center_info,
        'posts_info': posts_info,
        'all_count': all_count,
        'recommends': recommends
    }
    return render(request, 'search_info/major_info.html', context=context)


# 搜索学校中心
def searchCenter(request):
    keyWord = request.GET.get('search', '')
    school_info, major_info, center_info, posts_info, all_count, recommends = '', '', '', '', '', ''
    if keyWord:
        school_info = Schools.objects.filter(name__contains=keyWord)
        major_info = Majors.objects.filter(school__name__contains=keyWord)
        center_info = Centers.objects.filter(name__contains=keyWord)
        posts_info = Posts.objects.filter(post_title__contains=keyWord)
        recommends = Majors.objects.filter(is_recommend=1)
        all_count = school_info.count() + major_info.count() + center_info.count() + posts_info.count()

    # 分页展示
    data = center_info
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)
    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyWord,
        'school_info': school_info,
        'major_info': major_info,
        'center_info': center_info,
        'posts_info': posts_info,
        'all_count': all_count,
        'recommends': recommends
    }
    return render(request, 'search_info/center_info.html', context=context)


def searchNews(request):
    keyWord = request.GET.get('search', '')
    school_info, major_info, center_info, posts_info, all_count, recommends = '', '', '', '', '', ''
    if keyWord:
        school_info = Schools.objects.filter(name__contains=keyWord)
        major_info = Majors.objects.filter(school__name__contains=keyWord)
        center_info = Centers.objects.filter(name__contains=keyWord)
        posts_info = Posts.objects.filter(post_title__contains=keyWord)
        recommends = Majors.objects.filter(is_recommend=1)
        all_count = school_info.count() + major_info.count() + center_info.count() + posts_info.count()

    # 分页展示
    data = posts_info
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 15)
    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword': keyWord,
        'school_info': school_info,
        'major_info': major_info,
        'center_info': center_info,
        'posts_info': posts_info,
        'all_count': all_count,
        'recommends': recommends
    }
    return render(request, 'search_info/news_info.html', context=context)