# -*- coding: utf-8 -*-
# Create your views here.
from django.core.urlresolvers import reverse
from www.utils import packageResponse


class RESULT_CODE:
    SUCCESS = 0
    ERROR = -1


class RESULT_MESSAGE:
    NO_VIEWNAME = u'没有提供页面名称'
    INVALID_VIEWNAME = u'无效页面名称'
    SUCCESS = u'成功'


def djangoReverse(request):
    '''
    将django的reverse服务提供给javasript客户端访问
    警告:该接口使用逗号分隔串来传递url中需要应用的参数列表(args)，如果参数中含有逗号将要出现异常
    '''
    # 检查是否提供了参数
    if 'viewname' not in request.REQUEST:
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_VIEWNAME)
    viewname = request.REQUEST['viewname']

    # 处理url中的参数
    args = []
    if 'args' in request.REQUEST:
        argsString = request.REQUEST['args']
        if len(argsString) != 0:
            args = argsString.split(',')

    # 尝试做reverse解析
    try:
        url = reverse(viewname, args=args)
    except:
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.INVALID_VIEWNAME)

    # 将解析完的url返回客户端
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'url': url})

