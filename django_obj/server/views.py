from django.shortcuts import render
from .models import ServerCategorys, ServerPosts, Centers, AQuestions, Attachments
from django.http import HttpResponse, JsonResponse
from django.views import View
from cms.check import Base
from school.models import Schools
from major.models import MajorCates,Majors
from user.models import Provinces
import re
from major.pages import Page


def server_posts(request):
    server_posts = ServerPosts.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        server_posts = server_posts.filter(post_title__contains=keyword)
    server_post = server_posts
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, server_posts)
    context = {
        'data': pages['data'],
        'posts': server_post,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword,
    }
    return render(request, 'server/server_posts-list.html', context=context)


# 添加文章
class AddServerPost(View):
    def get(self, request):
        server_categorys = ServerCategorys.objects.filter(is_status=1)
        return render(request, 'server/server_posts-add.html', context={'cate': server_categorys})

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        sourceTitle = request.POST.get('sourceTitle')
        sourceUrl = request.POST.get('sourceUrl')
        keyWord = request.POST.get('keyWord')
        cate = request.POST.get('cate')

        if title == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入文章标题',
                'tagid': 'title'
            })
        else:
            ServerPosts.objects.create(
                post_title=title,
                post_content=content,
                source=sourceTitle,
                source_link=sourceUrl,
                keywords=keyWord,
                cateid_id=cate,
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': ''
            })


# 编辑文章
class EditServerPost(View):
    def get(self, request):
        ser_post_id = request.GET.get('post_id')
        post = ServerPosts.objects.get(id=ser_post_id)
        cate = ServerCategorys.objects.filter(is_status=1)
        # key_word = json.loads(post.keywords)
        context = {
            'post': post,
            'cate': cate,
            # 'keyword':key_word,
        }
        return render(request, 'server/server_posts-edit.html', context=context)

    def post(self, request):
        post_id = request.POST.get('post_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        sourceTitle = request.POST.get('sourceTitle')
        sourceUrl = request.POST.get('sourceUrl')
        keyWord = request.POST.get('keyWord')
        cate = request.POST.get('cate')
        count = request.POST.get('reader')

        if title == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入文章标题',
                'tagid': 'title'
            })
        else:
            info = ServerPosts.objects.get(id=post_id)
            info.post_title = title
            info.post_content = content
            info.source = sourceTitle
            info.source_link = sourceUrl
            info.keywords = keyWord
            info.cateid_id = cate
            info.edit_time = Base.getNowTime(request)
            info.views = count
            info.save()

            return JsonResponse({
                'status': 'success',
                'message': '修改成功',
                'info': ''
            })


# 删除文章
def del_ser_pos(request):
    post_id = request.GET.get('post_id')
    info = ServerPosts.objects.get(id=post_id)
    info.is_status = 0
    info.save()
    posts = ServerPosts.objects.filter(is_status=1)
    context = {
        'posts': posts
    }
    return render(request, 'server/server_posts-list.html', context=context)


# 已删除文章列表
def del_ser_list(request):
    server_posts = ServerPosts.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        server_posts = server_posts.filter(post_title__contains=keyword)
    server_post = server_posts
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, server_posts)
    context = {
        'data': pages['data'],
        'posts': server_post,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'server/server_del_posts-list.html', context=context)


# 恢复文章
def recover_server(request):
    post_id = request.GET.get('post_id')
    info = ServerPosts.objects.get(id=post_id)
    info.is_status = 1
    info.save()
    posts = ServerPosts.objects.filter(is_status=0)
    context = {
        'posts': posts
    }
    return render(request, 'server/server_del_posts-list.html', context=context)


# 彻底删除文章
def las_del_posts(request):
    post_id = request.GET.get('post_id')
    ServerPosts.objects.get(id=post_id).delete()
    posts = ServerPosts.objects.filter(is_status=0)
    return render(request, 'server/server_del_posts-list.html', context={'posts': posts})


# 服务中心分类
def server_cate(request):
    cate = ServerCategorys.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        cate = cate.filter(catename__contains=keyword)
    cates = cate
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, cate)
    context = {
        'data': pages['data'],
        'cate': cates,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'server/cate-list.html', context=context)


# 添加新分类
class AddCate(View):
    def get(self, request):
        return render(request, 'server/add_cate.html')

    def post(self, request):
        cateName = request.POST.get('cate_name')
        info = ServerCategorys.objects.filter(catename=cateName).exists()
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '当前分类已存在',
                'tagid': 'name'
            })
        else:
            ServerCategorys.objects.create(
                catename=cateName
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': ''
            })


# 编辑分类
class EditCate(View):
    def get(self, request):
        cate_id = request.GET.get('cate_id')
        cate = ServerCategorys.objects.get(id=cate_id)
        return render(request, 'server/edit_cate.html', context={'cate': cate})

    def post(self, request):
        cate_id = request.POST.get('cate_id')
        cateName = request.POST.get('cate_name')
        is_status = request.POST.get('is_status')
        info = ServerCategorys.objects.filter(catename=cateName).exists()

        cates = ServerCategorys.objects.get(id=cate_id)
        cates.catename = cateName
        cates.is_status = is_status
        cates.save()
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 删除分类
def del_cate(request):
    cate_id = request.GET.get('cate_id')
    info = ServerCategorys.objects.get(id=cate_id)
    info.is_status = 0
    info.save()
    cate = ServerCategorys.objects.filter(is_status=1)
    context = {
        'cate': cate
    }
    return render(request, 'server/cate-list.html', context=context)


# 已删除分类
def get_del_cate(request):
    cate = ServerCategorys.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        cate = cate.filter(catename__contains=keyword)
    cates = cate
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, cate)
    context = {
        'data': pages['data'],
        'cate': cates,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'server/del-cate.html', context=context)


# 恢复分类
def recover_cate(request):
    cate_id = request.GET.get('cate_id')
    info = ServerCategorys.objects.get(id=cate_id)
    info.is_status = 1
    info.save()
    cate = ServerCategorys.objects.filter(is_status=0)
    context = {
        'cate': cate
    }
    return render(request, 'server/del-cate.html', context=context)


# 彻底删除分类
def las_del_cate(request):
    cate_id = request.GET.get('cate_id')
    ServerCategorys.objects.get(id=cate_id).delete()
    cate = ServerCategorys.objects.filter(is_status=0)
    context = {
        'cate': cate
    }
    return render(request, 'server/del-cate.html', context=context)


# 学习中心
def center(request):
    center = Centers.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        center = center.filter(name__contains=keyword)
    centers = center
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, center)
    context = {
        'data': pages['data'],
        'center': centers,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }

    return render(request, 'server/center-list.html', context=context)


# 添加学习中心
class AddCenter(View):
    def get(self, request):
        provinces = Provinces.objects.all()
        schools = Schools.objects.filter(is_status=1)
        context = {
            'provinces':provinces,
            'schools':schools,
        }
        return render(request, 'server/add-center.html',context=context)

    def post(self, request):
        center_name = request.POST.get('center_name')
        num = request.POST.get('num')
        address = request.POST.get('address')
        school_code = request.POST.get('school')
        # 省份id
        prov_code = request.POST.get('prov')
        info = Centers.objects.filter(name=center_name).exists()
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '当前学习中心已存在',
                'tagid': 'name'
            })
        else:
            Centers.objects.create(
                name=center_name,
                num=num,
                address=address,
                school=Schools.objects.get(id=int(school_code)),
                provinces=Provinces.objects.get(id=int(prov_code))
            )
            return JsonResponse({
                'status': 'success',
                'message': '添加成功',
                'info': ''
            })


# 编辑学习中心
class EditCenter(View):
    def get(self, request):
        center_id = request.GET.get('center_id')
        center = Centers.objects.get(id=center_id)
        provinces = Provinces.objects.all()
        schools = Schools.objects.filter(is_status=1)
        context = {
            'center': center,
            'provinces': provinces,
            'schools': schools,
        }
        return render(request, 'server/edit_center.html', context=context)

    def post(self, request):
        center_id = request.POST.get('center_id')
        center_name = request.POST.get('center_name')
        school_code = request.POST.get('school')
        # 省份id
        prov_code = request.POST.get('prov')
        Centers.objects.filter(id=center_id).update(
            name=center_name,
            num=request.POST.get('num'),
            address=request.POST.get('address'),
            phone = request.POST.get('phone'),
            is_direct = request.POST.get('is_direct'),
            is_status = request.POST.get('is_status'),
            postcode = request.POST.get('post_code'),
            school=Schools.objects.get(id=int(school_code)),
            provinces=Provinces.objects.get(id=int(prov_code))
        )
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 删除学习中心
def delete_center(request):
    center_id = request.GET.get('center_id')
    Centers.objects.filter(id=center_id).update(
        is_status = 0
    )
    center = Centers.objects.filter(is_status=1)
    return render(request,'server/center-list.html',context={'center':center})


# 已删除学习中心
def del_center_list(request):
    center = Centers.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        center = center.filter(name__contains=keyword)
    centers = center
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, center)
    context = {
        'data': pages['data'],
        'center': centers,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }

    return render(request,'server/del_center-list.html',context=context)

# 恢复学习中心
def recover_center(request):
    center_id = request.GET.get('center_id')
    Centers.objects.filter(id=center_id).update(
        is_status = 1
    )
    center = Centers.objects.filter(is_status=0)
    context = {
        'center': center
    }
    return render(request, 'server/del_center-list.html', context=context)

# 彻底删除学习中心
def last_del_center(request):
    center_id = request.GET.get('center_id')
    Centers.objects.get(id=center_id).delete()
    center = Centers.objects.filter(is_status=0)
    context = {
        'center': center
    }
    return render(request, 'server/del_center-list.html', context=context)


# 附件管理
def get_enclosure(request):
    enclosure = Attachments.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        enclosure = enclosure.filter(name__contains=keyword)
    enclosures = enclosure
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, enclosure)
    context = {
        'data': pages['data'],
        'enclosure': enclosures,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }

    return render(request, 'server/enclosure-list.html', context=context)


# 上传附件
class AddEnclosure(View):
    def get(self,request):
        return render(request,'server/add_enclosure.html')

    def post(self,request):
        name = request.POST.get('name')
        file_name = request.FILES.get('file_name')
        info = Attachments.objects.filter(name=name).exists()
        if info:
            return JsonResponse({
                'status': 'fail',
                'message': '附件名已存在',
                'tagid': 'name'
            })
        if name == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入附件名',
                'tagid': 'name'
            })
        if file_name == None:
            return JsonResponse({
                'status': 'fail',
                'message': '请选择文件',
                'tagid': 'upload'
            })
        Attachments.objects.create(
            name=name,
            filename=file_name
        )
        return JsonResponse({
            'status':'success',
            'message':'文件上传成功',
            'info':''
        })


# 编辑附件
class EditEnclosure(View):
    def get(self,request):
        enclosure_id = request.GET.get('enclosure_id')
        enclosure = Attachments.objects.get(id=enclosure_id)
        context = {
            'enclosure':enclosure
        }
        return render(request,'server/edit_enclosure.html',context=context)

    def post(self,request):
        col_id = request.POST.get('id')
        name = request.POST.get('name')
        is_status = request.POST.get('is_status')
        file_name = request.FILES.get('file_name')
        if file_name:
            info = Attachments.objects.get(id=col_id)
            info.name=name
            info.filename = file_name
            info.is_status=is_status
            info.save()
            return JsonResponse({
                'status': 'success',
                'message': '文件修改成功',
                'info': ''
            })
        else:
            info = Attachments.objects.get(id=col_id)
            info.name=name
            info.is_status=is_status
            info.save()
            return JsonResponse({
                'status': 'success',
                'message': '文件修改成功',
                'info': ''
            })


# 删除附件
def del_enclosure(request):
    enc_id = request.GET.get('enc_id')
    enc = Attachments.objects.get(id=enc_id)
    enc.is_status = 0
    enc.save()
    enclosure = Attachments.objects.filter(is_status=1)
    context = {
        'enclosure': enclosure
    }
    return render(request, 'server/enclosure-list.html', context=context)


# 已删除附件
def get_del_enclosure(request):
    enclosure = Attachments.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        enclosure = enclosure.filter(name__contains=keyword)
    enclosures = enclosure
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, enclosure)
    context = {
        'data': pages['data'],
        'enclosure': enclosures,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request,'server/del_enclosure.html',context=context)


# 恢复附件
def recover_enclosure(request):
    enclosure_id = request.GET.get('enclosure_id')
    info = Attachments.objects.get(id=enclosure_id)
    info.is_status = 1
    info.save()
    enclosure = Attachments.objects.filter(is_status=0)
    context = {
        'enclosure': enclosure
    }
    return render(request, 'server/del_enclosure.html', context=context)


# 彻底删除附件
def las_del_enclosure(request):
    enc_id = request.GET.get('enc_id')
    Attachments.objects.get(id=enc_id).delete()
    enclosure = Attachments.objects.filter(is_status=0)
    context = {
        'enclosure': enclosure
    }
    return render(request, 'server/del_enclosure.html', context=context)



# 模拟题管理
def get_file(request):
    file = AQuestions.objects.filter(is_status=1)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        file = file.filter(name__contains=keyword)
    files = file
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, file)
    context = {
        'data': pages['data'],
        'file': files,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }

    return render(request, 'server/file-list.html', context=context)


# 添加模拟题
class AddQuest(View):
    def get(self,request):
        major_cate = MajorCates.objects.filter(is_status=1).exclude(pid=0)
        school = Schools.objects.filter(is_status=1)
        context = {
            'major_cate':major_cate,
            'school':school,
        }
        return render(request,'server/add_quest.html',context=context)

    def post(self,request):
        name = request.POST.get('name')
        school = request.POST.get('school')
        major = request.POST.get('major')
        level = request.POST.get('level')
        file_name = request.FILES.get('file_name')
        re_file = re.search('.*?\.(docx|doc|wps)',file_name.name)

        if name == '':
            return JsonResponse({
                'status':'fail',
                'message':'请输入名字',
                'tagid':'name'
            })
        if school == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请选择院校',
                'tagid': 'school'
            })
        if major == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请选择专业',
                'tagid': 'major'
            })
        if level == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请选择层次',
                'tagid': 'level'
            })
        if file_name == None:
            return JsonResponse({
                'status': 'fail',
                'message': '请选择文件',
                'tagid': 'upload'
            })
        if re_file == None:
            return JsonResponse({
                'status': 'fail',
                'message': '暂不支持此格式的文件，请上传doc,docx,wps后缀的文件',
                'tagid': 'upload'
            })
        else:
            AQuestions.objects.create(
                name=name,
                filename=file_name,
                school_id_id=school,
                major_cate_id_id=major,
                leval=level,
            )
            return JsonResponse({
                'status': 'success',
                'message': '上传成功',
                'info': ''
            })


# 编辑模拟题
class EditQuest(View):
    def get(self,request):
        quest_id = request.GET.get('quest_id')
        quest = AQuestions.objects.get(id=quest_id)
        major_cate = Majors.objects.filter(is_status=1).filter(school_id=quest.school_id)
        school = Schools.objects.filter(is_status=1)
        context = {
            'major_cate': major_cate,
            'school': school,
            'quest': quest
        }
        return render(request,'server/edit_quest.html',context=context)

    def post(self,request):
        ques_id = request.POST.get('quest_id')
        name = request.POST.get('name')
        school = request.POST.get('school')
        major = request.POST.get('major')
        level = request.POST.get('level')
        is_status = request.POST.get('is_status')
        file_name = request.FILES.get('file_name')


        if name == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请输入名字',
                'tagid': 'name'
            })
        if school == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请选择院校',
                'tagid': 'school'
            })
        if major == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请选择专业',
                'tagid': 'major'
            })
        if level == '':
            return JsonResponse({
                'status': 'fail',
                'message': '请选择层次',
                'tagid': 'level'
            })
        if file_name != None:
            re_file = re.search('.*?\.(docx|doc|wps)', file_name.name)
            if re_file == None:
                return JsonResponse({
                    'status': 'fail',
                    'message': '暂不支持此格式的文件，请上传doc,docx,wps后缀的文件',
                    'tagid': 'upload'
                })
        info = AQuestions.objects.get(id=ques_id)
        if file_name != None:
            info.filename = file_name
        else:
            info.name=name
            info.school_id_id=school
            info.major_cate_id_id=major
            info.leval=level
            info.is_status = is_status
        info.save()

        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 删除模拟题
def del_quest(request):
    quest_id = request.GET.get('quest_id')
    quest = AQuestions.objects.get(id=quest_id)
    quest.is_status = 0
    quest.save()
    file = AQuestions.objects.filter(is_status=1)
    context = {
        'file': file
    }
    return render(request, 'server/file-list.html', context=context)


# 已删除模拟题
def get_del_files(request):
    file = AQuestions.objects.filter(is_status=0)
    # 获取关键字
    keyword = request.GET.get('keyword', '')

    if keyword:
        file = file.filter(name__contains=keyword)
    files = file
    # 从前端获取当前的页码数
    page = request.GET.get('page', 1)
    pages = Page.get_page(request, page, file)
    context = {
        'data': pages['data'],
        'file': files,
        'paginator': pages['paginator'],
        'currentPage': pages['currentPage'],
        'page_range': pages['page_range'],
        'keyword':keyword
    }
    return render(request, 'server/del_file-list.html', context=context)


# 恢复模拟题
def recover_quest(request):
    quest_id = request.GET.get('quest_id')
    quest = AQuestions.objects.get(id=quest_id)
    quest.is_status = 1
    quest.save()
    file = AQuestions.objects.filter(is_status=0)
    context = {
        'file': file
    }
    return render(request, 'server/del_file-list.html', context=context)


# 彻底删除模拟题
def las_del_quest(request):
    quest_id = request.GET.get('quest_id')
    AQuestions.objects.get(id=quest_id).delete()
    file = AQuestions.objects.filter(is_status=0)
    context = {
        'file': file
    }
    return render(request, 'server/del_file-list.html', context=context)