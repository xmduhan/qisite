#-*- coding: utf-8 -*-

from django.http import HttpResponse
import json
from models import Paper
from django.forms import ValidationError
from datetime import datetime


def surveyAdd(request):
    pass


def surveyModify(request):
    pass


def surveyDelete(request):
    pass


class PaperAdd_ErrorMessage:
    no_login = u'没有登录'
    validation_error = u'数据校验错误'
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

    # 获取Paper模型中的所有属性
    fields = zip(*Paper._meta.get_fields_with_model())[0]
    keys = request.REQUEST.keys()
    data = {}
    for field in fields:
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue

        # 读取request数据
        value = request.REQUEST.get(field.name, None)

        # 对创建人和修改人的信息进行特殊处理
        if field.name in ('createBy', 'modifyBy'):
            value = user

        # 如果调用者没有显示执行字段值为空，则不增加到data中去，让模型的默认值发挥作用
        # 字段代码不能早于对createBy和modifyBy的处理
        if value == None and field.name not in keys:
            continue

        # 将校验的数据添加到data，准备为创建数据库用
        data[field.name] = value

    # 创建Paper对象
    paper = Paper(**data)
    try:
        paper.full_clean()
    except ValidationError as exception:
        result['errorCode'] = PaperAdd_ErrorCode.error
        result['errorMessage'] = PaperAdd_ErrorMessage.validation_error
        result['validationMessage'] = exception.message_dict
        return HttpResponse(json.dumps(result))

    # 保存到数据库
    paper.save()
    # 返回成功信息
    result['errorCode'] = PaperAdd_ErrorCode.success
    result['errorMessage'] = PaperAdd_ErrorMessage.success
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
