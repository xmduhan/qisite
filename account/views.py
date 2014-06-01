# -*- coding: utf-8 -*-
# Create your views here.

from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from account.models import User
from models import SmsCheckCode
import json, random, string
from interface import sms
from datetime import datetime, timedelta
import re


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


# sendSmsCheckCode 服务需要的常量定义
## 发送验证码的信息
checkCodeTextFormat = '您的注册验证码为%s，您可以它进行注册了。如果该信息不是您发送的，请忽略。'
## 手机号码格式定义
phonePattern = re.compile(r'^((13[0-9])|(15[^4,\D])|(14[57])|(17[0])|(18[0,0-9]))\d{8}$')
## 服务返回的出错信息定义
class sendSmsCheckCode_errorMessage:
    not_phone = '请提填写手机号码'
    invaild_phone = '输入的不是一个有效的手机号码'
    need_wait = '验证码已发送，%d秒后可以重发'
    send_sms_fail = '短信发送失败，请稍后重试'
    success = '发送成功'


def sendSmsCheckCode(request):
    # 读取request中的手机号码
    errorMessage = sendSmsCheckCode_errorMessage()
    result = {}
    if 'phone' not in request.REQUEST.keys():
        result['errorCode'] = -1
        result['errorMessage'] = errorMessage.not_phone
        return HttpResponse(json.dumps(result))

    # 检查输入是否符合手机格式
    phone = request.REQUEST['phone']
    if not phonePattern.match(phone):
        result['errorCode'] = -1
        result['errorMessage'] = errorMessage.invaild_phone
        return HttpResponse(json.dumps(result))

    # 是否符合发送的时间间隔
    interval = timedelta(minutes=3)
    smsCheckCodeList = SmsCheckCode.objects.filter(
        phone=phone, createTime__lte=datetime.now() - interval
    ).order_by("-createTime")
    if len(smsCheckCodeList) > 0:
        smsCheckCode = smsCheckCodeList[0]
        remain = datetime.now() - smsCheckCode.createTime - interval
        result['errorCode'] = -1
        result['errorMessage'] = errorMessage.need_wait % remain.seconds
        result['secondsRemain'] = remain.seconds
        return HttpResponse(json.dumps(result))

    # 生成并保存验证码
    checkCode = "".join(random.sample(string.digits, 6))
    SmsCheckCode(phone=phone, checkCode=checkCode).save()

    # 发送短信
    checkCodeText = checkCodeTextFormat % checkCode
    smsSendResult = sms.send(phone, checkCodeText)
    if smsSendResult['errorCode'] <> 0:
        result['errorCode'] = -1
        result['errorMessage'] = errorMessage.send_sms_fail
        return HttpResponse(json.dumps(result))

    # 返回成功
    result['errorCode'] = 0
    result['errorMessage'] = errorMessage.success
    return HttpResponse(json.dumps(result))