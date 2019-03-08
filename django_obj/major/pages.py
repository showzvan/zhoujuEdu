#-*-coding:utf-8-*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Page():
    def get_page(request,page,data):
        # 生成paginator对象, 定义每页显示7条记录
        paginator = Paginator(data, 7)
        currentPage = int(page)
        page_range = []
        try:
            data = paginator.page(page)  # 获取当前页码的记录
            current_page_num = data.number
            # 获取当前页码，前后两页的范围
            page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
                range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
            # 加上省略页码标记
            if page_range[0] - 1 >= 2:
                page_range.insert(0, '...')
            if paginator.num_pages - page_range[-1] >= 2:
                page_range.append('...')
        except PageNotAnInteger:
            data = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            current_page_num = data.number
            # 获取当前页码，前后两页的范围
            page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
                range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

            # 加上省略页码标记
            if page_range[0] - 1 >= 2:
                page_range.insert(0, '...')
            if paginator.num_pages - page_range[-1] >= 2:
                page_range.append('...')
        except EmptyPage:
            data = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

            # 如果一页中仅剩一条数据并且删除或回复的请况
            if len(data.object_list) % 7 == 0:
                currentPage = currentPage - 1
            current_page_num = data.number

            # 获取当前页码，前后两页的范围
            page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
                range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

            # 加上省略页码标记
            if page_range[0] - 1 >= 2:
                page_range.insert(0, '...')
            if paginator.num_pages - page_range[-1] >= 2:
                page_range.append('...')

        dir = {
            'paginator':paginator,
            'currentPage':currentPage,
            'data':data,
            'page_range':page_range,
        }

        return dir

