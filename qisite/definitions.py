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
    SURVEY_OBJECT_NOT_EXIST = u'调查对象不存在'
    QUESTION_OBJECT_NO_EXIST = u'问题对象不存在'
    BRANCH_OBJECT_NO_EXIST = u'选项对象不存在'
    NO_PRIVILEGE = u'没有权限操作该对象'
    NO_SURVEY_ID = u'需要提供调查对象的标志'
    TARGET_SURVEY_NEED_CUSTlIST = u'定向调查需要提供客户清单'
    CUSTLIST_OBJECT_NOT_EXIST = u'所指定的客户清单的对象不存在'
    ANSWER_COUNT_DIFF_WITH_QUESTION = u'提交问题的数量和问卷不一致'
    ANSWER_IS_MISSED_WHEN_REQUIRED = u'问题答案没有完整填写'
    QUESTION_NOT_IN_PAPER = u'提交问题的问题此问卷无关'
    BRANCH_NOT_IN_QUESTION = u'提交答案不在选项范围内'
    THANKS_FOR_ANSWER_SURVEY = u'提交完成，感谢您的参与!'

    SUCCESS = u'成功'