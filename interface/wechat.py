#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from xml.etree import ElementTree
from dicttoxml import dicttoxml

TOKEN = 'ZBAVckmvP9nyoxQ6bnUdXswahpU'  # 微信开发模式需要的加密参数


def securityCheck(request):
    '''
        检查请求是否发自微信的公众平台
    '''
    timestamp = request.REQUEST.get('timestamp', None)
    nonce = request.REQUEST.get('nonce', None)
    signature = request.REQUEST.get('signature', None)
    keys = [TOKEN, timestamp, nonce]
    keys.sort()
    calculated = hashlib.sha1(''.join(keys)).hexdigest()
    if signature == calculated:
        return True
    else:
        return False


def developConfirm(request):
    '''
        微信公众平台的开发者认证服务
    '''
    echostr = request.REQUEST.get('echostr', None)
    return HttpResponse(echostr)


def processTextMessage(data):
    pass


@csrf_exempt
def service(request):
    '''
        微信服务的中转器
    '''
    print '-------------------body---------------------'
    print request.body
    print '-------------------POST---------------------'
    print request.POST
    print '-------------------REQUEST---------------------'
    print request.REQUEST
    print '-------------------GET---------------------'
    print request.GET
    print '-------------------END---------------------'

    if not securityCheck(request):
        return HttpResponse('')

    # 如果使用get说明是开发者确认请求
    if request.method == 'GET':
        return developConfirm(request)

    if request.method == 'POST':
        # 读取服务器提交的数据
        pass
        #xmltree = ElementTree.fromstring(request.body)
        #data = {node.tag: node.text for node in xmltree}

        # 处理文本信息
        #if data == 'text':
        #    result = processTextMessage(data)
        #    return dicttoxml(result)


    # 对于所有不处理的类型返回空字符串
    return HttpResponse('')