#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views, services


urlpatterns = patterns(
    '',
    ####################################
    #              页面               #
    ####################################
    # 新增页面
    url(r'^view/survey/add/(?P<paperId>\d+)$', views.surveyAdd, name='view.survey.add'),
    url(r'^view/survey/add/action/', views.surveyAddAction, name='view.survey.add.action'),
    ## 列表页面
    url(r'^view/paper/list/$', views.paperList, name='view.paper.list'),
    url(r'^view/paper/list/(?P<page>\d+)$', views.paperList, name='view.paper.list'),
    url(r'^view/survey/list/$', views.surveyList, name='view.survey.list'),
    url(r'^view/survey/list/(?P<page>\d+)$', views.surveyList, name='view.survey.list'),
    url(r'^view/custList/list/$', views.custListList, name='view.custList.list'),
    url(r'^view/custList/list/(?P<page>\d+)$', views.custListList, name='view.custList.list'),
    ## 编辑页面
    url(r'^view/survey/edit/(?P<surveyId>\d+)$', views.surveyEdit, name='view.survey.edit'),
    url(r'^view/paper/edit/(?P<paperId>\d+)$', views.paperEdit, name='view.paper.edit'),
    url(r'^view/custList/edit/(?P<custListId>\d+)$', views.custListEdit, name='view.custList.edit'),
    url(r'^view/custList/edit/(?P<custListId>\d+)/(?P<page>\d+)$', views.custListEdit, name='view.custList.edit'),
    ## 获取问题编辑
    url(r'^view/question/edit/(?P<questionId>\S+)$', views.questionEdit, name='view.question.edit'),
    ## 答卷
    url(r'^view/survey/answer/all/(?P<surveyId>\d+)$', views.surveyAnswerAll, name='view.survey.answer'),
    url(r'^view/survey/answer/all/submit$', views.surveyAnswerAllSubmit, name='view.survey.answer.submit'),
    url(r'^view/survey/answer/step/(?P<surveyId>\d+)$', views.surveyAnswerStep, name='view.survey.answer.step'),
    url(r'^view/survey/answer/step/submit$', views.surveyAnswerStepSubmit, name='view.survey.answer.step.submit'),

    ## 样本导出
    url(r'^view/sample/export/(?P<surveyId>\d+)$', views.sampleExport, name='view.sample.export'),


    ## 调查发布页面
    url(r'^view/survey/publish/(?P<surveyId>\d+)$', views.surveyPublish, name='view.survey.publish'),
    url(r'^view/survey/imageCode/(?P<surveyId>\d+)$', views.surveyImageCode, name='view.survey.imageCode'),

    # 查看结果
    url(r'^view/survey/viewResult/(?P<surveyId>\d+)$', views.surveyViewResult, name='view.survey.viewResult'),

    ####################################
    #              服务               #
    ####################################
    ## survey
    url(r'^service/survey/add$', services.surveyAdd, name='service.survey.add'),
    url(r'^service/survey/modify$', services.surveyModify, name='service.survey.modify'),
    url(r'^service/survey/delete$', services.surveyDelete, name='service.survey.delete'),
    url(r'^service/survey/sendSurveyToPhone$', services.sendSurveyToPhone, name='service.survey.sendSurveyToPhone'),
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
    ## custList
    url(r'^service/custList/add$', services.custListAdd, name='service.custList.add'),
    url(r'^service/custList/delete$', services.custListDelete, name='service.custList.delete'),
    url(r'^service/custList/modify$', services.custListModify, name='service.custList.modify'),


    ## custListItem
    url(r'^service/custListItem/add$', services.custListItemAdd, name='service.custListItem.add'),
    url(r'^service/custListItem/delete$', services.custListItemDelete, name='service.custListItem.delete'),


)