#-*- coding: utf-8 -*-
USER_SESSION_NAME = 'user'
USER_CREATE_BY_FIELD_NAME = 'createBy'
USER_MODIFY_BY_FIELD_NAME = 'modifyBy'
CREATE_TIME_FIELD_NAME = 'createTime'
MODIFY_TIME_FIELD_NAME = 'modifyTime'

class RESULT_CODE:
    SUCCESS = 0
    ERROR = -1


class RESULT_MESSAGE:
    NO_LOGIN = u'没有登录'
    VALIDATION_ERROR = u'数据有效性校验失败'
    NO_ID = u'需要提供对象标识'
    BAD_SAGNATURE = u'数字签名无效'
    OBJECT_NOT_EXIST = u'对象不存在'
    NO_PRIVILEGE = u'没有权限操作该对象'
    SUCCESS = u'成功'