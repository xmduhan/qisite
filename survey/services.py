#-*- coding: utf-8 -*-
'''
    存在问题：
    1、对字段的处理，没有考虑外键、多对多关系、一对一关系。

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


def getModelFields(model):
    return zip(*model._meta.get_fields_with_model())[0]


def getForeignObject(field, id):
    return field.rel.to.objects.get(id=id)


def jsonBoolean2Python(jsonStringValue):
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
    keys = request.REQUEST.keys()
    data = {}
    #fields = zip(*Paper._meta.get_fields_with_model())[0]
    for field in getModelFields(Paper):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = request.REQUEST.get(field.name, None)

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
    paper_not_exist = u'该问卷已经删除了'
    no_privilege = u'没有权限修改'
    validation_error = u'数据校验错误'
    success = u'成功'


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

    # 检查对象是否还存在,并将对象锁定
    paperList = Paper.objects.filter(id=id).select_for_update()
    if len(paperList) == 0:
        result['errorCode'] = PaperModify_ErrorCode.error
        result['errorMessage'] = PaperModify_ErrorMessage.paper_not_exist
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


class PaperDelete_ErrorCode:
    success = 0
    error = -1


class PaperDelete_ErrorMessage:
    no_login = u'没有登录'
    no_id = u'需要提供问卷标识'
    bad_signature = u'数字签名被篡改'
    paper_not_exist = u'该问卷已经删除了'
    no_privilege = u'没有权限修改'
    validation_error = u'数据校验错误'
    success = u'成功'


def paperDelete(request):
    '''
        问卷删除服务
    '''
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = PaperDelete_ErrorCode.error
        result['errorMessage'] = PaperDelete_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了id
    keys = request.REQUEST.keys()
    if 'id' not in keys:
        result['errorCode'] = PaperDelete_ErrorCode.error
        result['errorMessage'] = PaperDelete_ErrorMessage.no_id
        return HttpResponse(json.dumps(result))
    idSigned = request.REQUEST['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = PaperDelete_ErrorCode.error
        result['errorMessage'] = PaperDelete_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 检查对象是否还存在,并将对象锁定
    paperList = Paper.objects.filter(id=id).select_for_update()
    if len(paperList) == 0:
        result['errorCode'] = PaperDelete_ErrorCode.error
        result['errorMessage'] = PaperDelete_ErrorMessage.paper_not_exist
        return HttpResponse(json.dumps(result))
    paper = paperList[0]

    # 检查当前用户是否有权限修改
    if paper.createBy.id != user.id:
        result['errorCode'] = PaperDelete_ErrorCode.error
        result['errorMessage'] = PaperDelete_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

    # 执行删除
    paper.delete()

    # 返回成功
    result['errorCode'] = PaperDelete_ErrorCode.success
    result['errorMessage'] = PaperDelete_ErrorMessage.success
    return HttpResponse(json.dumps(result))


class QuestionAdd_ErrorCode:
    success = 0
    error = -1


class QuestionAdd_ErrorMessage:
    success = u'成功'
    no_login = u'没有登陆'
    no_paper = u'需要提供要添加的问卷信息'
    bad_signature = u'数字签名被篡改'
    paper_no_exist = u'问卷已被删除'
    no_privilege = u'没有权限修改'
    validation_error = u'数据校验错误'


def questionAdd(request):
    '''
        为已有问卷增加一个问题的服务
    '''
    result = {}

    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = QuestionAdd_ErrorCode.error
        result['errorMessage'] = QuestionAdd_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否有提供paper
    keys = request.REQUEST.keys()
    if 'paper' not in keys:
        result['errorCode'] = QuestionAdd_ErrorCode.error
        result['errorMessage'] = QuestionAdd_ErrorMessage.no_paper
        return HttpResponse(json.dumps(result))
    paperIdSigned = request.REQUEST['paper']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        paperId = signer.unsign(paperIdSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = QuestionAdd_ErrorCode.error
        result['errorMessage'] = QuestionAdd_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 尝试读取paper信息
    paperList = Paper.objects.filter(id=paperId)
    if len(paperList) == 0:
        result['errorCode'] = QuestionAdd_ErrorCode.error
        result['errorMessage'] = QuestionAdd_ErrorMessage.paper_no_exist
        return HttpResponse(json.dumps(result))
    paper = paperList[0]

    # 检查是否有权限修改
    if paper.createBy.id != user.id:
        result['errorCode'] = QuestionAdd_ErrorCode.error
        result['errorMessage'] = QuestionAdd_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

    # 遍历Question的所有Field，并尝试在request中寻找是否提供了对应的数据
    data = {}
    for field in getModelFields(Question):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = request.REQUEST.get(field.name, None)
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
        result['errorCode'] = QuestionAdd_ErrorCode.error
        result['errorMessage'] = QuestionAdd_ErrorMessage.validation_error
        result['validationMessage'] = exception.message_dict
        return HttpResponse(json.dumps(result))

    # 写到数据库
    question.save()
    # 返回成功
    result['errorCode'] = QuestionAdd_ErrorCode.success
    result['errorMessage'] = QuestionAdd_ErrorMessage.success
    return HttpResponse(json.dumps(result))


class QuestionModify_ErrorCode:
    success = 0
    error = -1


class QuestionModify_ErrorMessage:
    no_login = u'没有登录'
    no_id = u'需要提供问卷标识'
    bad_signature = u'数字签名被篡改'
    question_not_exist = u'要修改的问题不存在'
    no_privilege = u'没有权限修该对象'
    validation_error = u'数据校验错误'
    success = u'成功'


def questionModify(request):
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = QuestionModify_ErrorCode.error
        result['errorMessage'] = QuestionModify_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了id
    keys = request.REQUEST.keys()
    if 'id' not in keys:
        result['errorCode'] = QuestionModify_ErrorCode.error
        result['errorMessage'] = QuestionModify_ErrorMessage.no_id
        return HttpResponse(json.dumps(result))
    idSigned = request.REQUEST['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = QuestionModify_ErrorCode.error
        result['errorMessage'] = QuestionModify_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 检查对象是否还存在
    questionList = Question.objects.filter(id=id).select_for_update()
    if len(questionList) == 0:
        result['errorCode'] = QuestionModify_ErrorCode.error
        result['errorMessage'] = QuestionModify_ErrorMessage.question_not_exist
        return HttpResponse(json.dumps(result))
    question = questionList[0]

    # 检查当前用户是否有权限修改
    if question.createBy.id != user.id:
        result['errorCode'] = QuestionModify_ErrorCode.error
        result['errorMessage'] = QuestionModify_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

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
        value = request.REQUEST.get(field.name, None)
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
        result['errorCode'] = QuestionModify_ErrorCode.error
        result['errorMessage'] = QuestionModify_ErrorMessage.validation_error
        result['validationMessage'] = exception.message_dict
        return HttpResponse(json.dumps(result))

    # 写到数据库
    question.save()
    # 返回成功
    result['errorCode'] = QuestionModify_ErrorCode.success
    result['errorMessage'] = QuestionModify_ErrorMessage.success
    return HttpResponse(json.dumps(result))


class QuestionDelete_ErrorCode:
    success = 0
    error = -1


class QuestionDelete_ErrorMessage:
    no_login = u'没有登录'
    no_id = u'需要提供问卷标识'
    bad_signature = u'数字签名被篡改'
    question_not_exist = u'要修改的问题不存在'
    no_privilege = u'没有权限修该对象'
    validation_error = u'数据校验错误'
    success = u'成功'


def questionDelete(request):
    '''
        问题删除服务
    '''
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = QuestionDelete_ErrorCode.error
        result['errorMessage'] = QuestionDelete_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了id
    keys = request.REQUEST.keys()
    if 'id' not in keys:
        result['errorCode'] = QuestionDelete_ErrorCode.error
        result['errorMessage'] = QuestionDelete_ErrorMessage.no_id
        return HttpResponse(json.dumps(result))
    idSigned = request.REQUEST['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = QuestionDelete_ErrorCode.error
        result['errorMessage'] = QuestionDelete_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 检查对象是否还存在
    questionList = Question.objects.filter(id=id).select_for_update()
    if len(questionList) == 0:
        result['errorCode'] = QuestionDelete_ErrorCode.error
        result['errorMessage'] = QuestionDelete_ErrorMessage.question_not_exist
        return HttpResponse(json.dumps(result))
    question = questionList[0]

    # 检查当前用户是否有权限修改
    if question.createBy.id != user.id:
        result['errorCode'] = QuestionDelete_ErrorCode.error
        result['errorMessage'] = QuestionDelete_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

    # 移动之后问题的排序号
    paper = question.paper
    questionList = paper.question_set.filter(question__ord__gt=question.ord).orderby('ord').select_for_update()
    for i, q in enumerate(questionList):
        q.ord = question.ord + i
        q.save()
    # 删除数据
    question.delete()

    # 返回成功
    result['errorCode'] = QuestionDelete_ErrorCode.success
    result['errorMessage'] = QuestionDelete_ErrorMessage.success
    return HttpResponse(json.dumps(result))


class BranchAdd_ErrorCode:
    error = -1
    success = 0


class BranchAdd_ErrorMessage:
    success = u'成功'
    no_login = u'没有登陆'
    no_question = u'需要指定要增加选项的问题'
    bad_signature = u'数字签名被篡改'
    question_no_exist = u'问题不存在'
    no_privilege = u'没有权限修改'
    validation_error = u'数据校验错误'


def branchAdd(request):
    '''
        为问题添加一个题支(选项）的服务
    '''
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = BranchAdd_ErrorCode.error
        result['errorMessage'] = BranchAdd_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否有提供Question
    keys = request.REQUEST.keys()
    if 'question' not in keys:
        result['errorCode'] = BranchAdd_ErrorCode.error
        result['errorMessage'] = BranchAdd_ErrorMessage.no_question
        return HttpResponse(json.dumps(result))
    questionIdSigned = request.REQUEST['question']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        questionId = signer.unsign(questionIdSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = BranchAdd_ErrorCode.error
        result['errorMessage'] = BranchAdd_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 尝试读取question信息
    questionList = Question.objects.filter(id=questionId)
    if len(questionList) == 0:
        result['errorCode'] = BranchAdd_ErrorCode.error
        result['errorMessage'] = BranchAdd_ErrorMessage.question_no_exist
        return HttpResponse(json.dumps(result))
    question = questionList[0]

    # 检查是否有权限做新增
    if question.createBy.id != user.id:
        result['errorCode'] = BranchAdd_ErrorCode.error
        result['errorMessage'] = BranchAdd_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

    # 遍历Branch的所有Field，并尝试在request中寻找是否提供了对应的数据
    data = {}
    for field in getModelFields(Branch):
        # 跳过系统自动增加的字段
        if field.auto_created:
            continue
        # 读取request数据
        value = request.REQUEST.get(field.name, None)
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
        result['errorCode'] = BranchAdd_ErrorCode.error
        result['errorMessage'] = BranchAdd_ErrorMessage.validation_error
        result['validationMessage'] = exception.message_dict
        return HttpResponse(json.dumps(result))

    # 写到数据库
    branch.save()
    # 返回成功
    result['errorCode'] = BranchAdd_ErrorCode.success
    result['errorMessage'] = BranchAdd_ErrorMessage.success
    return HttpResponse(json.dumps(result))


class BranchModify_ErrorCode:
    success = 0
    error = -1


class BranchModify_ErrorMessage:
    success = u'成功'
    no_login = u'没有登录'
    no_id = u'需要提供问卷标识'
    bad_signature = u'数字签名被篡改'
    branch_not_exist = u'要修改的问题不存在'
    no_privilege = u'没有权限修该对象'
    validation_error = u'数据校验错误'


def branchModify(request):
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = BranchModify_ErrorCode.error
        result['errorMessage'] = BranchModify_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了id
    keys = request.REQUEST.keys()
    if 'id' not in keys:
        result['errorCode'] = BranchModify_ErrorCode.error
        result['errorMessage'] = BranchModify_ErrorMessage.no_id
        return HttpResponse(json.dumps(result))
    idSigned = request.REQUEST['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = BranchModify_ErrorCode.error
        result['errorMessage'] = BranchModify_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 检查对象是否还存在
    branchList = Branch.objects.filter(id=id).select_for_update()
    if len(branchList) == 0:
        result['errorCode'] = BranchModify_ErrorCode.error
        result['errorMessage'] = BranchModify_ErrorMessage.branch_not_exist
        return HttpResponse(json.dumps(result))
    branch = branchList[0]

    # 检查当前用户是否有权限修改
    if branch.createBy.id != user.id:
        result['errorCode'] = BranchModify_ErrorCode.error
        result['errorMessage'] = BranchModify_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

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

        value = request.REQUEST.get(field.name, None)
        # 特殊处理json的Boolean型的变量
        if type(field) == BooleanField:
            value = jsonBoolean2Python(value)

        # 对外键的特殊处理
        if type(field) == ForeignKey:
            # 校验数字签名
            try:
                signer = Signer()
                value = signer.unsign(value)
            except BadSignature:
                # 篡改发现处理
                result['errorCode'] = BranchModify_ErrorCode.error
                result['errorMessage'] = BranchModify_ErrorMessage.bad_signature
                return HttpResponse(json.dumps(result))
            print '--1--'
            # id转化为对象
            value = getForeignObject(field, value)

        exec ('branch.%s = value' % field.name)

    # 特殊处理最近修改时间和最近修改用户
    branch.modifyBy = user
    branch.modifyTime = datetime.now()

    # 进行数据校验
    try:
        branch.full_clean()
    except ValidationError as exception:
        result['errorCode'] = BranchModify_ErrorCode.error
        result['errorMessage'] = BranchModify_ErrorMessage.validation_error
        result['validationMessage'] = exception.message_dict
        return HttpResponse(json.dumps(result))

    # 写到数据库
    branch.save()
    # 返回成功
    result['errorCode'] = BranchModify_ErrorCode.success
    result['errorMessage'] = BranchModify_ErrorMessage.success
    return HttpResponse(json.dumps(result))


class BranchDelete_ErrorCode:
    success = 0
    error = -1


class BranchDelete_ErrorMessage:
    success = u'成功'
    no_login = u'没有登录'
    no_id = u'需要提供问卷标识'
    bad_signature = u'数字签名被篡改'
    branch_not_exist = u'要修改的问题不存在'
    no_privilege = u'没有权限修该对象'
    validation_error = u'数据校验错误'


def branchDelete(request):
    result = {}
    # 检查用户是否登录，并读取session中的用户信息
    if USER_SESSION_NAME not in request.session.keys():
        result['errorCode'] = BranchDelete_ErrorCode.error
        result['errorMessage'] = BranchDelete_ErrorMessage.no_login
        return HttpResponse(json.dumps(result))
    user = request.session[USER_SESSION_NAME]

    # 检查是否提供了id
    keys = request.REQUEST.keys()
    if 'id' not in keys:
        result['errorCode'] = BranchDelete_ErrorCode.error
        result['errorMessage'] = BranchDelete_ErrorMessage.no_id
        return HttpResponse(json.dumps(result))
    idSigned = request.REQUEST['id']

    # 对id进行数字签名的检查
    try:
        signer = Signer()
        id = signer.unsign(idSigned)
    except BadSignature:
        # 篡改发现处理
        result['errorCode'] = BranchDelete_ErrorCode.error
        result['errorMessage'] = BranchDelete_ErrorMessage.bad_signature
        return HttpResponse(json.dumps(result))

    # 检查对象是否还存在
    branchList = Branch.objects.filter(id=id).select_for_update()
    if len(branchList) == 0:
        result['errorCode'] = BranchDelete_ErrorCode.error
        result['errorMessage'] = BranchDelete_ErrorMessage.branch_not_exist
        return HttpResponse(json.dumps(result))
    branch = branchList[0]

    # 检查当前用户是否有权限修改
    if branch.createBy.id != user.id:
        result['errorCode'] = BranchDelete_ErrorCode.error
        result['errorMessage'] = BranchDelete_ErrorMessage.no_privilege
        return HttpResponse(json.dumps(result))

        # 执行删除
    branch.delete()
    # 返回成功
    result['errorCode'] = BranchDelete_ErrorCode.success
    result['errorMessage'] = BranchDelete_ErrorMessage.success
    return HttpResponse(json.dumps(result))