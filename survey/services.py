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
    3、errorCode改成resultCode

'''
import json
from django.http import HttpResponse
from django.forms import ValidationError
from django.core.signing import Signer, BadSignature
from models import Paper, Question, Branch
from qisite.definitions import USER_SESSION_NAME, USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME, \
    CREATE_TIME_FIELD_NAME, MODIFY_TIME_FIELD_NAME
from datetime import datetime
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey
#from django.db import transaction

class RESULT_CODE:
    SUCCESS = 0
    ERROR = -1


class RESULT_MESSAGE:
    NO_LOGIN = u'没有登录'
    VALIDATION_ERROR = u'数据有效性校验失败'
    NO_ID = u'需要执行对象标识'
    BAD_SAGNATURE = u'数字签名无效'
    OBJECT_NOT_EXIST = u'对象不存在'
    NO_PRIVILEGE = u'没有权限操作该对象'
    SUCCESS = u'成功'


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


def packageResult(resultCode, resultMessage, others={}):
    '''
        将错误信息打包成为一个字典
    '''
    result = {}
    result['resultCode'] = resultCode
    result['resultMessage'] = resultMessage
    result = dict(result.items() + others.items())
    return result


def dictToJsonResponse(result):
    '''
        将一个字典转化为json结构的http返回数据
    '''
    return HttpResponse(json.dumps(result))


def packageResponse(resultCode, resultMessage, others={}):
    return dictToJsonResponse(packageResult(resultCode, resultMessage, others))


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


def surveyModify(request):
    pass


def surveyDelete(request):
    pass


def _paperAdd(data, user):
    pass


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
        result = packageResult(RESULT_CODE.ERROR, RESULT_MESSAGE.SUCCESS)
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
            value = paper.question_set.select_for_update().count() + 1
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
    questionList = paper.question_set.filter(question__ord__gt=question.ord).orderby('ord').select_for_update()
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
            value = question.branch_set.select_for_update().count() + 1
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
            if len(value) != 0:
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

    #
    print request.REQUEST

    # 检查是否提供了paper
    if 'paper' not in request.REQUEST.keys():
        return packageResponse(RESULT_CODE.ERROR, RESULT_MESSAGE.NO_ID)
    paperId = request.REQUEST['paper']

    # 调用问题新增处理过程
    requestData = {'paper': paperId, 'text': u'新增问题', 'type': 'Single'}
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
    return packageResponse(RESULT_CODE.SUCCESS, RESULT_MESSAGE.SUCCESS)



