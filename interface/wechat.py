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
    print 'timestamp =', timestamp
    nonce = request.REQUEST.get('nonce', None)
    print 'nonce =', nonce
    signature = request.REQUEST.get('signature', None)
    print 'signature =', signature
    echostr = request.REQUEST.get('echostr', None)
    print 'echostr =', echostr
    calculated = hashlib.sha1(''.join([TOKEN, timestamp, nonce])).hexdigest()
    if signature == calculated:
        print '----- success ------'
        return HttpResponse(echostr)
    else:
        print '----- error ------'
        return HttpResponse('no match!')


@csrf_exempt
def service(request):
    '''
        微信服务的中转器
    '''
    # 如果使用get说明是开发者确认请求
    if request.method == 'GET':
        return developerConfirm(request)

    return HttpResponse('ok')