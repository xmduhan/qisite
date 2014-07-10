#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse, Http404
from django.template import Context, loader, RequestContext
from account.models import User
from models import *
from django.core.signing import Signer, BadSignature
import services
from qisite.definitions import USER_SESSION_NAME


def getCurrent(request):
    #userList = User.objects.filter(name='杜涵')
    #if len(userList) > 0:
    #    return userList[0]
    #else:
    #    return None
    return request.session.get(USER_SESSION_NAME, None)


def surveyList(request):
    '''
        列出用户的调查
    '''
    user = getCurrent(request)
    surveyList = user.surveyCreated_set.all()
    #surveyList = user.surveyCreated_set.filter(state = 'P')
    template = loader.get_template('survey/surveyList.html')
    context = RequestContext(request, {"surveyList": surveyList, 'session': request.session})
    return HttpResponse(template.render(context))


def surveyEdit(request):
    '''
        编辑调查
    '''
    template = loader.get_template('survey/surveyEdit.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def paperList(request):
    '''
        列出用户的问卷
    '''
    user = getCurrent(request)
    paperList = user.paperCreated_set.all()
    template = loader.get_template('survey/paperList.html')
    context = RequestContext(request, {"paperList": paperList, 'session': request.session})
    return HttpResponse(template.render(context))
'''
from survey.models import *
from account.models import *
from django.core.paginator import Paginator
user = User.objects.filter(phone='13599900875')[0]
p = Paginator(user.paperCreated_set.all(),5)
p.num_pages
p.count
for i in p.page(2):
    print i
'''


def paperEdit(request, paperId):
    '''
        问卷编辑
    '''
    paperList = Paper.objects.filter(id=paperId)
    if paperList:
        paper = paperList[0]
        template = loader.get_template('survey/paperEdit.html')
        context = RequestContext(request, {'session': request.session, 'paper': paper})
        return HttpResponse(template.render(context))
    else:
        raise Http404


def custListList(request):
    '''
        列出用户的客户清单
    '''
    user = getCurrent(request)
    custListList = user.custListCreated_set.all()
    template = loader.get_template('survey/custListList.html')
    context = RequestContext(request, {'custListList': custListList, 'session': request.session})
    return HttpResponse(template.render(context))


def questionEdit(request, questionId):
    '''
        生成问题编辑DOM片段的view服务
    '''
    user = getCurrent(request)

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





