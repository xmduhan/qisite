# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json


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