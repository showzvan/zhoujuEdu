from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . models import Posts,Tag
from django.views import View
from school.models import Schools
from cms.check import Base
from major.pages import Page


def get_posts(request):
    posts = Posts.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        posts = posts.filter(post_title__contains=keyword)
    post = posts
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, posts)
    context = {
        'data': pages['data'],
        'posts': post,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'posts/posts-list.html',context=context)

# 删除文章
def del_posts(request):
    post_id = request.GET.get('post_id')
    post = Posts.objects.get(id=post_id)
    post.is_status = 0
    post.save()
    posts = Posts.objects.filter(is_status=1)
    context = {
        'posts': posts
    }
    return render(request,'posts/posts-list.html',context=context)


# 已删除文章
def get_del(request):
    posts = Posts.objects.filter(is_status=0)
    post = posts
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, posts)
    context = {
        'data': pages['data'],
        'posts': post,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range']
    }
    return render(request,'posts/posts-del.html',context=context)


# 恢复文章
def recover_post(request):
    post_id = request.GET.get('post_id')
    Posts.objects.filter(id=post_id).update(is_status = 1)
    info = Posts.objects.filter(is_status=0)
    context = {
        'posts': info
    }
    return render(request, 'posts/posts-del.html', context=context)


# 彻底删除文章
def last_del_post(request):
    post_id = request.GET.get('post_id')
    Posts.objects.filter(id=post_id).delete()
    info = Posts.objects.filter(is_status=0)
    context = {
        'posts': info
    }
    return render(request, 'posts/posts-del.html', context=context)


# 添加文章
class AddPosts(View):
    def get(self,request):
        tags = Tag.objects.all()
        school = Schools.objects.filter(is_status=1)
        return render(request,'posts/posts-add.html',context={
            'tag':tags,
            'school':school
        })

    def post(self,request):
        article_avatar = request.FILES.get('avatar')
        content = request.POST.get('content')
        title = request.POST.get('title')
        sourceTitle = request.POST.get('sourceTitle')
        sourceUrl = request.POST.get('sourceUrl')
        tag = request.POST.get('tags')
        school = request.POST.get('school',None)
        if school == '':
            school = None

        if title == '':
            return JsonResponse({
                'status':'fail',
                'message':'请输入文章标题',
                'tagid':'title'
            })
        Posts.objects.create(
            post_title=title,
            post_image=article_avatar,
            source=sourceTitle,
            source_link=sourceUrl,
            post_content=content,
            edit_time=Base.getNowTime(request),
            school_id=school,
            tags_id=tag
        )
        return JsonResponse({
            'status':'success',
            'message':'添加成功',
            'info':'',
        })


# 编辑文章
class EditPost(View):
    def get(self,request):
        post_id = request.GET.get('post_id')
        post = Posts.objects.get(id=post_id)
        tags = Tag.objects.all()
        school = Schools.objects.filter(is_status=1)
        context = {
            'post':post,
            'tag':tags,
            'school':school
        }
        return render(request,'posts/posts-edit.html',context=context)

    def post(self,request):
        post_id = request.POST.get('post_id')
        article_avatar = request.FILES.get('avatar')
        print(article_avatar)
        content = request.POST.get('content')
        title = request.POST.get('title')
        sourceTitle = request.POST.get('sourceTitle')
        sourceUrl = request.POST.get('sourceUrl')
        count = request.POST.get('count')
        tag = request.POST.get('tags')
        school = request.POST.get('school', None)
        if article_avatar != None:
            pos = Posts.objects.get(id=post_id)
            pos.post_image = article_avatar
            pos.save()
        if school == '':
            school = None

        if title == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入文章标题',
                'tagid': 'title'
            })
        Posts.objects.filter(id=post_id).update(
            post_title=title,
            source=sourceTitle,
            source_link=sourceUrl,
            post_content=content,
            edit_time=Base.getNowTime(request),
            views=count,
            school_id=school,
            tags_id=tag
        )
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': '',
        })