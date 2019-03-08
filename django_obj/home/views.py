from django.shortcuts import render
from major.models import MajorCates
from school.models import Schools
from detail.models import Links

def home(request):
    major_cate = MajorCates.objects.order_by('id').filter(is_status=1).filter(pid=0)
    cate_all = MajorCates.objects.order_by('id').filter(is_status=1)
    schools = Schools.objects.filter(is_status=1)
    links = Links.objects.filter(is_status=1)
    context = {
        'major_cate':major_cate,
        'cate_all':cate_all,
        'schools':schools,
        'links':links
    }
    return render(request, 'home/index_1.html',context=context)
