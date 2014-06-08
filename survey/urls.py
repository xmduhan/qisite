#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^view/survey/list$', views.surveyList, name='view.survey.list'),
    url(r'^view/custList/list$', views.custListList, name='view.custList.list'),
    url(r'^view/paper/list$', views.paperList, name='view.paper.list'),
    # 编辑
    url(r'^view/survey/edit$', views.surveyEdit, name='view.survey.edit'),
    url(r'^view/paper/edit/(?P<paperId>\d+)$', views.paperEdit, name='view.paper.edit'),

)