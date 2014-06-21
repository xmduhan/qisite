#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse, Http404
from django.template import Context, loader, RequestContext
from account.models import User
from models import *
from django.core.signing import Signer, BadSignature


def getCurrent():
    userList = User.objects.filter(name='杜涵')
    if len(userList) > 0:
        return userList[0]
    else:
        return None


def surveyList(request):
    user = getCurrent()
    surveyList = user.surveyCreated_set.all()
    #surveyList = user.surveyCreated_set.filter(state = 'P')
    template = loader.get_template('survey/surveyList.html')
    context = RequestContext(request, {"surveyList": surveyList, 'session': request.session})
    return HttpResponse(template.render(context))


def surveyEdit(request):
    template = loader.get_template('survey/surveyEdit.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def paperList(request):
    user = getCurrent()
    paperList = user.paperCreated_set.all()
    template = loader.get_template('survey/paperList.html')
    context = RequestContext(request, {"paperList": paperList, 'session': request.session})
    return HttpResponse(template.render(context))


def paperEdit(request, paperId):
    paperList = Paper.objects.filter(id=paperId)
    if paperList:
        paper = paperList[0]
        template = loader.get_template('survey/paperEdit.html')
        context = RequestContext(request, {'session': request.session, 'paper': paper})
        return HttpResponse(template.render(context))
    else:
        raise Http404


def custListList(request):
    user = getCurrent()
    custListList = user.custListCreated_set.all()
    template = loader.get_template('survey/custListList.html')
    context = RequestContext(request, {'custListList': custListList, 'session': request.session})
    return HttpResponse(template.render(context))


def questionEdit(request, questionId):
    '''
        生成问题编辑DOM片段的view服务
    '''
    user = getCurrent()

    # 检查数字签名
    try:
        sign = Signer()
        questionIdUnsigned = sign.unsign(questionId)
    except BadSignature as bs:
        raise Http404

    # 根据id查询问题对象
    question = Question.objects.get(id=questionIdUnsigned)

    # 检查用户是否权限查看该对象
    if question.createBy != user:
        raise Http404

    # 返回数据
    template = loader.get_template('survey/question/question.html')
    context = RequestContext(request, {'question': question})
    return HttpResponse(template.render(context))


