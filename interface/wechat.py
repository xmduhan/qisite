#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from xml.etree import ElementTree
from dicttoxml import dicttoxml
from datetime import datetime

TOKEN = 'ZBAVckmvP9nyoxQ6bnUdXswahpU'  # 微信开发模式需要的加密参数


def datetimeToInt(date):
    return (date - datetime(1970, 1, 1)).total_seconds()


def securityCheck(request):
    '''
        检查请求是否发自微信的公众平台
    '''
    timestamp = request.REQUEST.get('timestamp', '')
    nonce = request.REQUEST.get('nonce', '')
    signature = request.REQUEST.get('signature', '')
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
    return HttpResponse(request.REQUEST.get('echostr', ''))


def processTextMessage(data):
    # 读取消息信息
    toUserName = data.get('ToUserName', '')  ##开发者微信号
    fromUserName = data.get('FromUserName', '')  #发送方帐号（一个OpenID）
    createTime = data.get('CreateTime', '')  #消息创建时间 （整型）
    msgType = data.get('MsgType', '')  #text
    content = data.get('Content', '')  #文本消息内容
    msgId = data.get('MsgId', '')  #消息id，64位整型

    # 打包返回信息
    result = {
        'ToUserName': fromUserName,
        'FromUserName': toUserName,
        'CreateTime': datetimeToInt(datetime.now()),
        'MsgType': msgType,
        'Content': content
    }
    return result


@csrf_exempt
def service(request):
    '''
        微信服务的中转器
    '''

    # 检查是否微信公众平台发出的请求
    if not securityCheck(request):
        return HttpResponse('')

    # 如果使用get说明是开发者确认请求
    if request.method == 'GET':
        return developConfirm(request)

    if request.method == 'POST':
        # 读取服务器提交的数据
        xmltree = ElementTree.fromstring(request.body)
        data = {node.tag: node.text for node in xmltree}

        msgType = data.get('MsgType', '')

        # 处理文本信息
        if msgType == 'text':
            result = processTextMessage(data)
            if len(result) == 0:
                return HttpResponse('')
            else:
                print dicttoxml(result)
                return HttpResponse(dicttoxml(result))

    # 对于所有不处理的类型返回空字符串
    return HttpResponse('')