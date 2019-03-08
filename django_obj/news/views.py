from django.shortcuts import render
from posts.models import Posts,Tag
from major.models import Majors
from school.models import Schools
from choose_major.pages import Page


def news(request):
    posts = Posts.objects.order_by('-id').filter(is_status=1)
    # 热门文章
    hot_posts = Posts.objects.order_by('-views').filter(is_status=1)[:10]

    # 分页展示
    data = posts
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, data, 20)
    context = {
        'data': pages['data'],
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'posts':posts,
        'hot_posts':hot_posts,
    }
    return render(request,'news/posts.html',context=context)


def news_detail(request,posts_id):
    # 查询相关文章
    post = Posts.objects.get(id=posts_id)
    # 获取热门文章
    hot_posts = Posts.objects.order_by('-views').filter(is_status=1)[:10]
    # 获取热招专业
    hot_majors = Majors.objects.filter(is_status=1).order_by('-count')[:5]
    # 热门院校
    hot_school = Schools.objects.order_by('-count').filter(is_status=1)[:15]

    # previous post 上一篇
    pre_posts = Posts.objects.filter(is_status=1).filter(id__gt=post.id).order_by('id')
    if pre_posts.count() > 0:
        pre_post = pre_posts[0]
    else:
        pre_post = None

    # next post 下一篇
    next_posts = Posts.objects.filter(is_status=1).filter(id__lt=post.id).order_by('-id')
    if next_posts.count() > 0:
        next_post = next_posts[0]
    else:
        next_post = None

    # 增加一次阅读量
    views = int(post.views) + 1
    post.views = views
    post.save()

    context = {
        'post':post,
        'hot_posts':hot_posts,
        'hot_majors':hot_majors,
        'pre_post':pre_post,
        'next_post':next_post,
        'hot_school':hot_school
    }
    return render(request,'news/posts-detail.html',context=context)