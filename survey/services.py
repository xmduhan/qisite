#-*- coding: utf-8 -*-
'''
    设计原则：
    1、最小管辖范围原则，

    2、请求接受和处理分来
        使得具体处理过程可以被其他服务直接通过调用访问，而不是直接向服务器发起请求。

    存在问题：
    1、对字段的处理，没有考虑外键、多对多关系、一对一关系。

    重构队列：
    1、检查用户是否登录部分
    2、数字前签名的检查部分

'''
import json
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.core.signing import Signer, BadSignature
from models import Paper, Question, Branch, Survey, CustList, CustListItem
from qisite.definitions import USER_SESSION_NAME, USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME, \
    CREATE_TIME_FIELD_NAME, MODIFY_TIME_FIELD_NAME
from qisite.utils import updateModelInstance
from datetime import datetime
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey
#from django.db import transaction
from www.utils import packageResult, dictToJsonResponse, packageResponse
from qisite.settings import smsSend
from qisite.settings import domain

from qisite.definitions import RESULT_CODE, RESULT_MESSAGE


def getModelFields(model):
    '''
        通过一个模型获取其内部定义的所有字段(Field)
    '''
    return zip(*model._meta.get_fields_with_model())[0]


def getForeignObject(field, id):
    '''
        根据一个外键定义和一个对象id找到对应的对象实例
    '''
    return field.rel.to.objects.get(id=id)


def jsonBoolean2Python(jsonStringValue):
    '''
        将json的布尔字串表达转化为json结构
    '''
    if jsonStringValue in ('true', 'false'):
        return jsonStringValue.capitalize()
    else:
        return jsonStringValue


def surveyAdd(request):
    pass


def _surveyModify(requestData, user):
    '''
      处理问卷修改的具体过程
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']
    print idSigned

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    surveyList = Survey.objects.filter(id=id).select_for_update()
    if len(surveyList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    survey = surveyList[0]

    # 检查当前用户是否有权限修改
    if survey.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 遍历每一个字段，检查是否提供修改信息，如果有则将器修改
    fields = zip(*Survey._meta.get_fields_with_model())[0]
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
        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)
        # 执行修改
        exec ('survey.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    survey.modifyBy = user
    survey.modifyTime = datetime.now()

    # 进行数据校验
    try:
        survey.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict}
        )
    # 写到数据库
    survey.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def surveyModify(request):
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _surveyModify(requestData, user)
    return dictToJsonResponse(result)


def _surveyDelete(requestData, user):
    '''
    问卷删除的具体处理函数
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    surveyList = Survey.objects.filter(id=id).select_for_update()
    if len(surveyList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    survey = surveyList[0]

    # 检查当前用户是否有权限修改
    if survey.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 执行删除
    # 调查的删除不是直接删除，而是将状态改为P，有些信息还要以备后查
    survey.state = 'P'
    survey.save()

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def surveyDelete(request):
    '''
        问卷调查服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _surveyDelete(requestData, user)
    return dictToJsonResponse(result)


def _paperAdd(requestData, user):
    '''
        新增一个问卷的具体处理过程
    '''
    # 获取Paper模型中的所有属性
    keys = requestData.keys()
    data = {}
    #fields = zip(*Paper._meta.get_fields_with_model())[0]
    for field in getModelFields(Paper):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = requestData.get(field.name, None)

        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)

        # 对创建人和修改人的信息进行特殊处理
        if field.name in [USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME]:
            value = user
        # 如果调用者没有显示执行字段值为空，则不增加到data中去，让模型的默认值发挥作用
        # 字段代码不能早于对createBy和modifyBy的处理
        if value is None and field.name not in keys:
            continue
        # 将校验的数据添加到data，准备为创建数据库用
        data[field.name] = value
    paper = Paper(**data)

    # 校验数据
    try:
        paper.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict})
    # 保存到数据库
    paper.save()
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'paperId': paper.id})


def paperAdd(request):
    '''
        创建问卷的功能服务
    '''

    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _paperAdd(requestData, user)
    return dictToJsonResponse(result)


def _paperModify(requestData, user):
    '''
      处理问卷修改的具体过程
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    paperList = Paper.objects.filter(id=id).select_for_update()
    if len(paperList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    paper = paperList[0]

    # 检查当前用户是否有权限修改
    if paper.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

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
        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)
        # 执行修改
        exec ('paper.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    paper.modifyBy = user
    paper.modifyTime = datetime.now()

    # 进行数据校验
    try:
        paper.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict}
        )

    # 写到数据库
    paper.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def paperModify(request):
    '''
        问卷基本信息修改服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _paperModify(requestData, user)
    return dictToJsonResponse(result)


def _paperDelete(requestData, user):
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    paperList = Paper.objects.filter(id=id).select_for_update()
    if len(paperList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    paper = paperList[0]

    # 检查当前用户是否有权限修改
    if paper.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 执行删除
    paper.delete()

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def paperDelete(request):
    '''
        问卷删除服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _paperDelete(requestData, user)
    return dictToJsonResponse(result)


def _questionAdd(requestData, user):
    '''
        为已有文件增加一个问题的处理过程
    '''
    # 检查是否有提供paper
    keys = requestData.keys()
    if 'paper' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    paperIdSigned = requestData['paper']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        paperId = signer.unsign(paperIdSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 尝试读取paper信息
    paperList = Paper.objects.filter(id=paperId)
    if len(paperList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    paper = paperList[0]

    # 检查是否有权限修改
    if paper.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 遍历Question的所有Field，并尝试在request中寻找是否提供了对应的数据
    data = {}
    for field in getModelFields(Question):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)
        # 对创建人和修改人的信息进行特殊处理
        if field.name in [USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME]:
            value = user
        # 对paper字段进行特殊处理,提交的数据是id转化为对象
        if field.name == 'paper':
            value = paper
        # 对ord 字段进行特殊处理，取当前的问题数量加1
        if field.name == 'ord':
            # 这里锁定了paper所有question对象
            value = paper.question_set.select_for_update().count()
            # 如果调用者没有显示执行字段值为空，则不增加到data中去，让模型的默认值发挥作用
        # 字段代码不能早于对createBy和modifyBy的处理
        if value is None and field.name not in keys:
            continue
        # 将校验的数据添加到data，准备为创建数据库用
        data[field.name] = value
    question = Question(**data)

    # 进行数据校验
    try:
        question.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR,
            {'validationMessage': exception.message_dict}
        )
    # 写到数据库
    question.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'questionId': question.id})


def questionAdd(request):
    '''
        为已有问卷增加一个问题的服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    # 调用过程具体处理过程
    result = _questionAdd(requestData, user)
    return dictToJsonResponse(result)


def _questionModify(requestData, user):
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在
    questionList = Question.objects.filter(id=id).select_for_update()
    if len(questionList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    question = questionList[0]

    # 检查当前用户是否有权限修改
    if question.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 遍历每一个字段，检查是否提供修改信息，如果有则将器修改
    fields = zip(*Question._meta.get_fields_with_model())[0]
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
        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)
        # 执行修改
        exec ('question.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    question.modifyBy = user
    question.modifyTime = datetime.now()

    # 进行数据校验
    try:
        question.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR,
            {'validationMessage': exception.message_dict})

    # 写到数据库
    question.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def questionModify(request):
    '''
        问题修改的后台服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _questionModify(requestData, user)
    return dictToJsonResponse(result)


def _questionSetOrd(requestData, user):
    """
    """
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查是否提供了有效的Ord号
    if 'newOrd' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.INVALID_ORD)

    try:
        newOrd = int(requestData['newOrd'])
    except:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.INVALID_ORD)

    # 检查对象是否还存在
    questionList = Question.objects.filter(id=id).select_for_update()
    if len(questionList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    question = questionList[0]

    # 检查提供的排序号是否在有效范围内
    paper = question.paper
    questionCount = paper.question_set.count()
    if ( newOrd < 0 ) or ( newOrd >= questionCount ):
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.INVALID_ORD)

    # 调用问题的ord设置方法
    question.setOrd(newOrd)

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def questionSetOrd(request):
    """
    重新设置一个问题在问卷中的顺序
    request参数:
    id 对应的问题id,已通过数字签名进行加密
    newOrd 问题的新排序号
    """
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _questionSetOrd(requestData, user)
    return dictToJsonResponse(result)


def _questionDelete(requestData, user):
    '''
        问题删除的具体处理过程
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在
    questionList = Question.objects.filter(id=id).select_for_update()
    if len(questionList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    question = questionList[0]

    # 检查当前用户是否有权限修改
    if question.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 移动之后问题的排序号
    paper = question.paper
    questionList = paper.question_set.filter(ord__gt=question.ord).order_by('ord').select_for_update()
    for i, q in enumerate(questionList):
        q.ord = question.ord + i
        q.save()
    # 删除数据
    question.delete()

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def questionDelete(request):
    '''
        问题删除服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _questionDelete(requestData, user)
    return dictToJsonResponse(result)


def _branchAdd(requestData, user):
    '''
        增加一个选项的具体处理过程
    '''
    # 检查是否有提供Question
    keys = requestData.keys()
    if 'question' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    questionIdSigned = requestData['question']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        questionId = signer.unsign(questionIdSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 尝试读取question信息
    questionList = Question.objects.filter(id=questionId)
    if len(questionList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    question = questionList[0]

    # 检查是否有权限做新增
    if question.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 遍历Branch的所有Field，并尝试在request中寻找是否提供了对应的数据
    data = {}
    for field in getModelFields(Branch):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)
        # 对创建人和修改人的信息进行特殊处理
        if field.name in [USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME]:
            value = user
        # 对question字段进行特殊处理,提交的数据是id转化为对象
        if field.name == 'question':
            value = question
        # 对ord 字段进行特殊处理，取当前的问题数量加1
        if field.name == 'ord':
            # 这里锁定了question所有branch对象
            value = question.branch_set.select_for_update().count()
            # 如果调用者没有显示执行字段值为空，则不增加到data中去，让模型的默认值发挥作用
        # 字段代码不能早于对createBy和modifyBy的处理
        if value is None and field.name not in keys:
            continue
        # 将校验的数据添加到data，准备为创建数据库用
        data[field.name] = value
    branch = Branch(**data)

    # 进行数据校验
    try:
        branch.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR,
            {'validationMessage': exception.message_dict})

    # 写到数据库
    branch.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'branchId': branch.id})


def branchAdd(request):
    '''
        为问题添加一个题支(选项）的服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _branchAdd(requestData, user)
    return dictToJsonResponse(result)


def _branchModify(requestData, user):
    '''
        选项修改具体处理过程
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在
    branchList = Branch.objects.filter(id=id).select_for_update()
    if len(branchList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    branch = branchList[0]

    # 检查当前用户是否有权限修改
    if branch.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 遍历每一个字段，检查是否提供修改信息，如果有则将器修改
    fields = zip(*Branch._meta.get_fields_with_model())[0]
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

        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)

        # 对外键的特殊处理
        if type(field) == ForeignKey:
            if len(value) != 0 and value != 'null':
                # 校验数字签名
                try:
                    signer = Signer()
                    value = signer.unsign(value)
                except BadSignature:
                    # 篡改发现处理
                    return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)
                # id转化为对象
                value = getForeignObject(field, value)
            else:
                value = None

        exec ('branch.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    branch.modifyBy = user
    branch.modifyTime = datetime.now()

    # 进行数据校验
    try:
        branch.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict})


    # 写到数据库
    branch.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def branchModify(request):
    '''
        选项修改的服务
    '''

    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _branchModify(requestData, user)
    return dictToJsonResponse(result)


def _branchDelete(requestData, user):
    '''
        选项删除的具体处理过程
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在
    branchList = Branch.objects.filter(id=id).select_for_update()
    if len(branchList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    branch = branchList[0]

    # 检查当前用户是否有权限修改
    if branch.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 处理之后的选项编号向前移动
    question = branch.question
    branchList = question.branch_set.filter(ord__gt=branch.ord).order_by('ord').select_for_update()
    for i, b in enumerate(branchList):
        b.ord = branch.ord + i
        b.save()
    # 执行删除
    branch.delete()

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def branchDelete(request):
    '''
        选项删除的具体处理过程
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _branchDelete(requestData, user)
    return dictToJsonResponse(result)


def addDefaultSingleQuestion(request):
    '''
        增加一个默认结构的单选题，提供给前台的新增问题按钮使用。
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了paper
    if 'paper' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    paperId = request.REQUEST['paper']

    # 调用问题新增处理过程
    requestData = {'paper': paperId, 'text': u'新增单选题', 'type': 'Single'}
    result = _questionAdd(requestData, user)
    if result['resultCode'] != 0:
        return dictToJsonResponse(result)
    questionId = result['questionId']

    # 对id进行数字签名
    signer = Signer()
    questionId = signer.sign(questionId)

    # 增加两个默认选项
    for i in [1, 2]:
        requestData = {'question': questionId, 'text': u'选项%d' % i}
        result = _branchAdd(requestData, user)
        if result['resultCode'] != 0:
            return dictToJsonResponse(result)

    # 返回成功
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'id': questionId})


def addDefaultMultipleQuestion(request):
    '''
        增加一个默认结构的多选题，提供给前台的新增问题按钮使用。
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了paper
    if 'paper' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    paperId = request.REQUEST['paper']

    # 调用问题新增处理过程
    requestData = {'paper': paperId, 'text': u'新增多选题', 'type': 'Multiple'}
    result = _questionAdd(requestData, user)
    if result['resultCode'] != 0:
        return dictToJsonResponse(result)
    questionId = result['questionId']

    # 对id进行数字签名
    signer = Signer()
    questionId = signer.sign(questionId)

    # 增加两个默认选项
    for i in [1, 2, 3, 4]:
        requestData = {'question': questionId, 'text': u'选项%d' % i}
        result = _branchAdd(requestData, user)
        if result['resultCode'] != 0:
            return dictToJsonResponse(result)

    # 返回成功
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'id': questionId})

def addDefaultTextQuestion(request):
    '''
        增加一个默认结构的问答题，提供给前台的新增问题按钮使用。
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了paper
    if 'paper' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    paperId = request.REQUEST['paper']

    # 调用问题新增处理过程
    requestData = {'paper': paperId, 'text': u'新增问答题', 'type': 'Text'}
    result = _questionAdd(requestData, user)
    if result['resultCode'] != 0:
        return dictToJsonResponse(result)
    questionId = result['questionId']

    # 对id进行数字签名
    signer = Signer()
    questionId = signer.sign(questionId)

    # 返回成功
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'id': questionId})



def addDefaultScoreQuestion(request):
    '''
        增加一个默认结构的问答题，提供给前台的新增问题按钮使用。
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了paper
    if 'paper' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    paperId = request.REQUEST['paper']

    # 调用问题新增处理过程
    requestData = {'paper': paperId, 'text': u'新增评分题', 'type': 'Score'}
    result = _questionAdd(requestData, user)
    if result['resultCode'] != 0:
        return dictToJsonResponse(result)
    questionId = result['questionId']

    # 对id进行数字签名
    signer = Signer()
    questionId = signer.sign(questionId)

    # 返回成功
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'id': questionId})


def addDefaultBranch(request):
    '''
        增加一个默认选项的服务，提供给界面的新增选项按钮用
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了question
    if 'question' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    questionId = request.REQUEST['question']

    # 调用新增选项的处理过程
    requestData = {'question': questionId, 'text': u'新增选项'}
    result = _branchAdd(requestData, user)
    return dictToJsonResponse(result)


def getReachableQuestionListForSelect(request):
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了branchId
    if 'branchId' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    branchIdSigned = request.REQUEST['branchId']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        branchId = signer.unsign(branchIdSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在
    branchList = Branch.objects.filter(id=branchId).select_for_update()
    if len(branchList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    branch = branchList[0]

    # 检查当前用户是否有权限修改
    if branch.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 将数据打包
    questionList = []
    # 导入问卷内的所有可选问题
    for question in branch.getReachableQuestionList():
        questionList.append({
            'num': question.getNum(),
            'id': question.getIdSigned(),
            'selected': question == branch.nextQuestion,
            'type': question.type
        })

    # 导入系统预定义
    for question in branch.getSystemPredefined():
        questionList.append({
            'num': question.getNum(),
            'id': question.getIdSigned(),
            'selected': branch.nextQuestion == question,
            'type': question.type
        })

    # 导入为空是系统预定义的下一题
    questionList.append({
        'num': '下一题',
        'id': None,
        'selected': branch.nextQuestion is None,
        'type': None
    })
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'questionList': questionList})


def _custListAdd(requestData, user):
    '''
        新增一个问卷的具体处理过程
    '''
    # 获取custList模型中的所有属性
    keys = requestData.keys()
    data = {}
    #fields = zip(*CustList._meta.get_fields_with_model())[0]
    for field in getModelFields(CustList):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = requestData.get(field.name, None)

        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)

        # 对创建人和修改人的信息进行特殊处理
        if field.name in [USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME]:
            value = user
        # 如果调用者没有显示执行字段值为空，则不增加到data中去，让模型的默认值发挥作用
        # 字段代码不能早于对createBy和modifyBy的处理
        if value is None and field.name not in keys:
            continue
        # 将校验的数据添加到data，准备为创建数据库用
        data[field.name] = value
    custList = CustList(**data)

    # 校验数据
    try:
        custList.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict})
    # 保存到数据库
    custList.save()
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'custListId': custList.id})


def custListAdd(request):
    '''
        创建问卷的功能服务
    '''

    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _custListAdd(requestData, user)
    return dictToJsonResponse(result)


def _custListDelete(requestData, user):
    '''
    问卷删除的具体处理函数
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    custListList = CustList.objects.filter(id=id).select_for_update()
    if len(custListList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    custList = custListList[0]

    # 检查当前用户是否有权限修改
    if custList.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 执行删除
    custList.delete()

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def custListDelete(request):
    '''
        问卷调查服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _custListDelete(requestData, user)
    return dictToJsonResponse(result)


def _custListModify(requestData, user):
    '''
      处理问卷修改的具体过程
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']
    print idSigned

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    custListList = CustList.objects.filter(id=id).select_for_update()
    if len(custListList) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    custList = custListList[0]

    # 检查当前用户是否有权限修改
    if custList.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 遍历每一个字段，检查是否提供修改信息，如果有则将器修改
    fields = zip(*CustList._meta.get_fields_with_model())[0]
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
        value = requestData.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)
        # 执行修改
        exec ('custList.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    custList.modifyBy = user
    custList.modifyTime = datetime.now()

    # 进行数据校验
    try:
        custList.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict}
        )
    # 写到数据库
    custList.save()
    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def custListModify(request):
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _custListModify(requestData, user)
    return dictToJsonResponse(result)


def _custListItemAdd(requestData, user):
    '''
        新增一个问卷的具体处理过程
    '''
    # 检查custListId是否存在
    custListIdSigned = requestData.get('custList')
    if not custListIdSigned:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)

    # 进行数字签名的检查
    try:
        signer = Signer()
        custListId = signer.unsign(custListIdSigned)
    except:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 尝试读取custList对象
    try:
        custList = CustList.objects.get(id=custListId)
    except:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)

    # 检查用户是否有权限
    if custList.createBy != user:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)


    # 通过request提供的数据创建custListItem对象
    custListItem = CustListItem()
    updateModelInstance(custListItem, requestData, tryUnsigned=True)

    # 处理当前用户
    custListItem.createBy = user
    custListItem.modifyBy = user

    # 校验数据
    try:
        custListItem.full_clean()
    except ValidationError as exception:
        return packageResult(
            RESULT_CODE.ERROR, RESULT_MESSAGE.VALIDATION_ERROR, {'validationMessage': exception.message_dict})

    # 保存到数据库
    custListItem.save()
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'custListItemId': custListItem.id})


def custListItemAdd(request):
    '''
        创建问卷的功能服务
    '''

    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _custListItemAdd(requestData, user)
    return dictToJsonResponse(result)


def _custListItemDelete(requestData, user):
    '''
    问卷删除的具体处理函数
    '''
    # 检查是否提供了id
    keys = requestData.keys()
    if 'id' not in keys:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)

    # 检查对象是否还存在,并将对象锁定
    custListListItem = CustListItem.objects.filter(id=id).select_for_update()
    if len(custListListItem) == 0:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
    custListItem = custListListItem[0]

    # 检查当前用户是否有权限修改
    if custListItem.createBy.id != user.id:
        return packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)

    # 执行删除
    custListItem.delete()

    # 返回成功
    return packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)


def custListItemDelete(request):
    '''
        问卷调查服务
    '''
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]
    requestData = request.REQUEST
    result = _custListItemDelete(requestData, user)
    return dictToJsonResponse(result)


def sendSurveyToPhone(request):
    '''
    将推荐链接短信发送到手机的服务
    '''

    # 检查用户是否存在
    if USER_SESSION_NAME not in request.session.keys():
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_LOGIN)
        return dictToJsonResponse(result)
    user = request.session[USER_SESSION_NAME]

    #
    requestData = request.REQUEST

    # 尝试获取调查对象的标识
    keys = requestData.keys()
    if 'id' not in keys:
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
        return dictToJsonResponse(result)
    idSigned = requestData['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.BAD_SAGNATURE)
        return dictToJsonResponse(result)

    # 加载对象
    surveyList = Survey.objects.filter(id=id, state='A').select_for_update()
    if len(surveyList) == 0:
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.OBJECT_NOT_EXIST)
        return dictToJsonResponse(result)
    survey = surveyList[0]

    # 检查当前用户是否权限
    if survey.createBy != user:
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_PRIVILEGE)
        return dictToJsonResponse(result)

    # 读取要发送的信息
    keys = requestData.keys()
    if 'message' not in keys:
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_MESSAGE)
        return dictToJsonResponse(result)
    message = requestData['message']

    # 检查短信内容是否包含访问连接
    url = domain + reverse('survey:view.survey.answer.render', args=[survey.id])
    if url not in message:
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.URL_NO_IN_MESSAGE)
        return dictToJsonResponse(result)

    # 检查上次短信发送时间
    timeDelaySeconds = 120
    if survey.lastSmsSendTime:
        delta = datetime.now() - survey.lastSmsSendTime
        if delta.seconds <= timeDelaySeconds:
            secondsRemain = timeDelaySeconds - delta.seconds
            result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.NEED_WAIT, {'secondsRemain': secondsRemain})
            return dictToJsonResponse(result)

    # 更新最后发送时间
    survey.lastSmsSendTime = datetime.now()
    survey.save()

    # 尝试发送短信
    try:
        smsSendResult = smsSend(user.phone, message)
        if smsSendResult['resultCode'] != 0:
            result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.FAIL_TO_SEND_SMS)
            return dictToJsonResponse(result)
    except Exception as e:
        print e
        raise
    # 返回成功
    result = packageResult(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS, {'secondsRemain': timeDelaySeconds})
    return dictToJsonResponse(result)







