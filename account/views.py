# -*- coding: utf-8 -*-
# Create your views here.

from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from account.models import User


def register(request):
    template = loader.get_template('account/register.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def login(request):
    logined = False
    errorMessage = ''
    keys = request.REQUEST.keys()
    if 'phone' in keys and 'password' in keys:
        phone = request.REQUEST['phone']
        password = request.REQUEST['password']
        if phone and password:
            userList = User.objects.filter(phone=phone)
            if userList:
                #print "password : %s " % password
                user = userList[0]
                check = check_password(password, user.password)
                if check:
                    # 把用户信息放到session中去
                    request.session['user'] = user
                    logined = True
                else:
                    errorMessage = '手机号或密码不正确'
            else:
                errorMessage = '该手机号码还未注册过'
        else:
            errorMessage = '请提供用户名和密码'
    #else:
    #通过连接访问,不需要提示错误
    if logined:
        # 如果登录成功返回首页
        template = loader.get_template('www/index.html')
        context = RequestContext(request, {'session': request.session})
        return HttpResponse(template.render(context))
    else:
        # 没有登录成功返回登录页面
        template = loader.get_template('account/login.html')
        context = RequestContext(request, {'errorMessage': errorMessage})
        return HttpResponse(template.render(context))


def logout(request):
    session = request.session
    if 'user' in session.keys():
        del session['user']
    template = loader.get_template('www/index.html')
    context = RequestContext(request, {'session': session})
    return HttpResponse(template.render(context))


def recovery(request):
    session = request.session
    template = loader.get_template('account/recovery.html')
    context = RequestContext(request, {'session': session})
    return HttpResponse(template.render(context))