#-*- coding: utf-8 -*-

from django.http import HttpResponse
import json
from models import Paper


def surveyAdd(request):
    pass


def surveyModify(request):
    pass


def surveyDelete(request):
    pass


class PaperAdd_ErrorMessage:
    no_login = u'没有登录'
    no_title = u'需要提供标题'
    success = u'成功'
    unknown = u'未知'


class PaperAdd_ErrorCode:
    success = 0
    error = -1


def paperAdd(request):
    '''
        创建问卷的功能服务
    '''
    result = {}

    # 检查用户是否登录，并读取session中的用户信息
    if 'user' not in request.session.keys():
        result['errorCode'] = PaperAdd_ErrorCode.error
        result['errorMessage'] = PaperAdd_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session['user']

    # 检查是否提供了标题，创建一个问卷至少要提供标题
    if 'title' not in request.REQUEST.keys():
        result['errorCode'] = PaperAdd_ErrorCode.error
        result['errorMessage'] = PaperAdd_ErrorMessage.no_title
        return HttpResponse(json.dumps(result))
    title = request.REQUEST['title']

    # 读取description信息
    description = None
    inOrder = None
    questionNumStyle = None
    lookBack = None
    paging = None

    Paper(
        title=title, description=description,
        questionNumStyle=questionNumStyle,
        inOrder=inOrder, lookBack=lookBack, paging=paging,
        createBy=user, modifyBy=user
    ).save()


    # 创建成功
    result['errorCode'] = PaperAdd_ErrorCode.success
    result['errorMessage'] = PaperAdd_ErrorMessage.no_login
    return HttpResponse(json.dumps(result))


def paperModify(request):
    pass


def paperDelete(request):
    pass


def questionAdd(request):
    pass


def questionModify(request):
    pass


def questionDelete(request):
    pass


def branchAdd(request):
    pass


def branchModify(request):
    pass


def branchDelete(request):
    pass
