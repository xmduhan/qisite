#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views, services


urlpatterns = patterns(
    '',
    ####################################
    #              页面               #
    ####################################
    ## 列表页面
    url(r'^view/survey/list$', views.surveyList, name='view.survey.list'),
    url(r'^view/custList/list$', views.custListList, name='view.custList.list'),
    url(r'^view/paper/list/$', views.paperList, name='view.paper.list'),
    url(r'^view/paper/list/(?P<page>\d+)$', views.paperList, name='view.paper.list'),
    ## 编辑页面
    url(r'^view/survey/edit$', views.surveyEdit, name='view.survey.edit'),
    url(r'^view/paper/edit/(?P<paperId>\d+)$', views.paperEdit, name='view.paper.edit'),
    ## 获取问题编辑
    url(r'^view/question/edit/(?P<questionId>\S+)$', views.questionEdit, name='view.question.edit'),

    ####################################
    #              服务               #
    ####################################
    ## survey
    url(r'^service/survey/add$', services.surveyAdd, name='service.survey.add'),
    url(r'^service/survey/modify$', services.surveyModify, name='service.survey.modify'),
    url(r'^service/survey/delete$', services.surveyDelete, name='service.survey.delete'),
    ## paper
    url(r'^service/paper/add$', services.paperAdd, name='service.paper.add'),
    url(r'^service/paper/modify$', services.paperModify, name='service.paper.modify'),
    url(r'^service/paper/delete$', services.paperDelete, name='service.paper.delete'),
    ## question
    url(r'^service/question/add$', services.questionAdd, name='service.question.add'),
    url(r'^service/question/modify$', services.questionModify, name='service.question.modify'),
    url(r'^service/question/delete$', services.questionDelete, name='service.question.delete'),
    url(r'^service/question/addDefaultSingleQuestion$', services.addDefaultSingleQuestion,
        name='service.question.addDefaultSingleQuestion'),
    ## branch
    url(r'^service/branch/add$', services.branchAdd, name='service.branch.add'),
    url(r'^service/branch/modify$', services.branchModify, name='service.branch.modify'),
    url(r'^service/branch/delete$', services.branchDelete, name='service.branch.delete'),
    url(r'^service/branch/addDefaultBranch$', services.addDefaultBranch, name='service.branch.addDefaultBranch'),
    url(r'^service/branch/getReachableQuestionListForSelect$', services.getReachableQuestionListForSelect,
        name='service.branch.getReachableQuestionListForSelect'),
)