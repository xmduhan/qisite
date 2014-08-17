#-*- coding: utf-8 -*-

from django.db.models.fields import BooleanField
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.core.signing import Signer, BadSignature
from definitions import USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME, CREATE_TIME_FIELD_NAME, \
    MODIFY_TIME_FIELD_NAME
from dateutil import parser
defaultExcludeFields = ['id', USER_CREATE_BY_FIELD_NAME, USER_MODIFY_BY_FIELD_NAME, CREATE_TIME_FIELD_NAME,
                        MODIFY_TIME_FIELD_NAME]

stringMeanTrue = ['true', 'on', '1', '是', u'是', 'yes']
stringMeanFalse = ['false', 'off', '0', '否', u'否', 'no']
stringMeanNone = ['null', 'none', 'nil', '', u'空', '空']


def stringToBool(s):
    '''
    将字符转化为布尔型
    '''
    if s.lower() in stringMeanTrue:
        return True
    if s.lower() in stringMeanFalse:
        return False
    raise Exception('无法识别的布尔字符串')


def getForeignObject(field, id):
    '''
    根据一个外键定义和一个对象id找到对应的对象实例
    '''
    return field.rel.to.objects.get(id=id)


def updateModelInstance(modelInst, dataDict, excludeFields=defaultExcludeFields, tryUnsigned=False):
    '''
    通过一个字典更新一个model实例的方法
    虽然我们可以用Model(**dataDict)和Model.objects.filter(pk=pk).update(**dataDict)方法来实现更新此功能，
    但是有时我们处理的是来自request的数据时还是会遇到很多的困扰，比如bool型的数据被表示成'true'和'false'，
    还有就是外键被表示成一个id等问题，还有日期格式的甄别处理。
    '''
    model = modelInst.__class__
    fields = zip(*model._meta.get_fields_with_model())[0]
    signer = Signer()
    for field in fields:
        # 不处理id,创建人,创建时间等字段
        if field.auto_created or field.name in excludeFields:
            continue

        # 如果field不再提供的数据中就不处理
        if not field.name in dataDict:
            continue

        # 读取数据字段中存放的值
        value = dataDict[field.name]

        # 特殊处理bool型的数据
        if type(field) == BooleanField:
            if type(value) in [str, unicode]:
                value = stringToBool(value)

        # 外键的特殊处理
        if type(field) == ForeignKey:
            if type(value) in [int, float]:
                value = getForeignObject(field, value)
            if type(value) in [str, unicode]:
                if value.lower() not in stringMeanNone:
                    # 如果指定了tryUnsigned,尝试检查id是否是数字签名过的
                    if tryUnsigned:
                        try:
                            valueUnsigned = signer.unsign(value)
                            value = valueUnsigned
                        except BadSignature:
                            pass
                    # 调用外键加载过程
                    value = getForeignObject(field, value)
                else:
                    value = None

        # 处理日期
        if type(field) == DateTimeField:
            if type(value) in [str, unicode]:
                if len(value) == 0:
                    continue
                value = parser.parse(value)

        exec ('modelInst.%s = value' % field.name)

    return modelInst



