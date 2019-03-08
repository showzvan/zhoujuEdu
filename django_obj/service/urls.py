#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views


app_name = 'service'
urlpatterns = [
    path('',views.service,name='service'),
    re_path('show-(?P<service_id>\d+)',views.post_detail,name='post_detail'),
    path('help/',views.help,name='help'),
    path('sign/',views.sign,name='sign'),
    path('new_exam/',views.new_exam,name='new_exam'),
    path('exam/',views.exam,name='exam'),
    path('graduation/',views.graduation,name='graduation'),
    path('feecard/',views.Feecard.as_view(),name='feecard'),
    path('center/',views.Center.as_view(),name='center'),
    # 学习中心查询
    path('center_search/',views.CenterSearch.as_view(),name='center_search'),
    path('collegeautho/',views.Collegeautho.as_view(),name='collegeautho'),
    # 院校授权查询
    path('collegeautho-search/',views.CollegeauthoSearch,name='collegeautho-search'),
    path('examdownload/',views.Examdownload.as_view(),name='examdownload'),
    path('courseware/',views.courseware,name='courseware'),
    path('sch_form/',views.sch_form,name='sch_form'),
    path('application/',views.application,name='application'),
    path('getmajorlist/',views.get_major,name='get_major'),
    path('getlevellist/',views.get_level,name='get_level'),
]