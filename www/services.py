# -*- coding: utf-8 -*-
# Create your views here.
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse


class RESULT_CODE:
    SUCCESS = 0
    ERROR = -1


class RESULT_MESSAGE:
    NO_VIEWNAME = u'没有提供页面名称'
    INVALID_VIEWNAME = u'无效页面名称'
    SUCCESS = u'成功'


def djangoReverse(request):
    viewname = request.REQUEST('viewname')
    url = reverse(viewname)
    result = {'url': url}

