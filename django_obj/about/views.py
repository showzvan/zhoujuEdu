from django.shortcuts import render
from django.http import HttpResponse
from detail.models import Links


def index(request):
    return render(request, 'about/about-index.html')
    # return render(request,'about/about-index.html')


def contact(request):
    return render(request,'about/about-lianxiwomen.html')


def fv(request):
    return render(request,'about/about-fv.html')


def agreement(request):
    return render(request,'about/about-xieyi.html')


def links(request):
    links = Links.objects.filter(is_status=1)
    context = {
        'links':links
    }
    return render(request,'about/about-links.html',context=context)