#-*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.forms import ValidationError
from django.core.signing import Signer, BadSignature

from models import Paper
from qisite.definitions import USER_SESSION_NAME, USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME, \
    CREATE_TIME_FIELD_NAME, MODIFY_TIME_FIELD_NAME
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
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = PaperAdd_ErrorCode.error
        result['errorMessage'] = PaperAdd_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

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
        if field.name in [USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME]:
            value = user

        # 如果调用者没有显示执行字段值为空，则不增加到data中去，让模型的默认值发挥作用
        # 字段代码不能早于对createBy和modifyBy的处理
        if value is None and field.name not in keys:
            continue

        # 将校验的数据添加到data，准备为创建数据库用
        data[field.name] = value

    # 校验数据
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


class PaperModify_ErrorCode:
    success = 0
    error = -1


class PaperModify_ErrorMessage:
    no_login = u'没有登录'
    no_id = u'需要提供问卷标识'
    bad_signature = u'数字签名被篡改'
    paper_deleted = u'该问卷已经删除了'
    no_privilege = u'没有权限修改'
    validation_error = u'数据校验错误'


def paperModify(request):
    '''
        问卷基本信息修改服务
    '''
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了id
    keys = request.REQUEST.keys()
    if 'id' not in keys:
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.no_id
        return HttpResponse(json.dumps(result))
    idSigned = request.REQUEST['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 检查对象是否还存在
    paperList = Paper.objects.filter(id=id)
    if len(paperList) == 0:
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.paper_deleted
        return HttpResponse(json.dumps(result))
    paper = paperList[0]

    # 检查当前用户是否有权限修改
    if paper.createBy.id != user.id:
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

    # 遍历每一个字段，检查是否提供修改信息，如果有则将器修改
    fields = zip(*Paper._meta.get_fields_with_model())[0]
    for field in fields:
        # 不能修改自动增加字段和id字段
        if field.auto_created or field.name == 'id':
            continue
        # 对应字段没有提供修改信息就跳过。
        if field.name not in keys:
            continue
        # 创建与修改的时间和用户不能由客户端来修改
        if field.name in [USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME, CREATE_TIME_FIELD_NAME,
                          MODIFY_TIME_FIELD_NAME]:
            continue
        # 读取客户提供的新值
        value = request.REQUEST.get(field.name, None)
        # 执行修改
        eval('paper.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    paper.modifyBy = user
    paper.modifyTime = datetime.now()

    # 进行数据校验
    try:
        paper.full_clean()
    except ValidationError as exception:
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.validation_error
        result['validationMessage'] = exception.message_dict
        return HttpResponse(json.dumps(result))

    # 写到数据库
    paper.save()
    # 返回成功
    result['errorCode'] = PaperModify_ErrorCode.success
    result['errorMessage'] = PaperModify_ErrorMessage.success
    return HttpResponse(json.dumps(result))


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
