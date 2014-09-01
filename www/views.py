# -*- coding: utf-8 -*-
# Create your views here.
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse


def index(request):
    '''
    首页
    '''
    template = loader.get_template('www/index.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def help(request):
    '''
    帮助页面
    '''
    template = loader.get_template('www/help.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def confirmDialog(request):
    '''
    确认框的DOM数据
    '''
    template = loader.get_template('www/dialog/confirmDialog.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def messageDialog(request):
    '''
    消息框的DOM数据
    '''
    template = loader.get_template('www/dialog/messageDialog.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def message(request):
    '''
    出错提示测试
    '''
    template = loader.get_template('www/message.html')
    context = RequestContext(
        request, {'title': '测试标题', 'message': '测试消息', 'returnUrl': '/'})
    return HttpResponse(template.render(context))

