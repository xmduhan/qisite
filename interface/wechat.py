#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib


TOKEN = 'ZBAVckmvP9nyoxQ6bnUdXswahpU'  # 微信开发模式需要的加密参数


def developerConfirm(request):
    '''
        微信公众平台的开发者认证服务
    '''
    timestamp = request.REQUEST.get('timestamp', None)
    nonce = request.REQUEST.get('nonce', None)
    signature = request.REQUEST.get('signature', None)
    echostr = request.REQUEST.get('echostr', None)
    keys = [TOKEN, timestamp, nonce]
    keys.sort()
    calculated = hashlib.sha1(''.join(keys)).hexdigest()
    if signature == calculated:
        return HttpResponse(echostr)
    else:
        return HttpResponse('no match!')


@csrf_exempt
def service(request):
    '''
        微信服务的中转器
    '''
    # 如果使用get说明是开发者确认请求
    if request.method == 'GET':
        return developerConfirm(request)

    # 返回空字串，表示对此类型不处理
    return HttpResponse('')