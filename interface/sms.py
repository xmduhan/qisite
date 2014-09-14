#-*- coding: utf-8 -*-
import urllib, urllib2


uid = 'joerge'
key = '664bf7c1849b3e6331c1'
smsServerUrl = "http://utf8.sms.webchinese.cn"
resultMessage = {
    -1, '没有该用户账户',
    -2, '接口密钥不正确',
    -21, 'MD5接口密钥加密不正确',
    -3, '短信数量不足',
    -11, '该用户被禁用',
    -14, '短信内容出现非法字符',
    -4, '手机号格式不正确',
    -41, '手机号码为空',
    -42, '短信内容为空',
    -51, '短信签名格式不正确',
}


def send(phone, text):
    '''
    短信接口格式
    #http://utf8.sms.webchinese.cn/?Uid=本站用户名&Key=接口安全密码&smsMob=手机号码&smsText=短信内容
    '''
    # 对短信的内容进行字符集转化
    if type(text) == unicode:
        smsText = text.encode('utf-8')
    else:
        # 这里可能还需要将非utf-8的str转化为utf-8(暂缺)
        smsText = text

    # 打包url数据
    data = {"Uid": uid, "Key": key, "smsMob": phone, "smsText": smsText}
    postData = urllib.urlencode(data)

    # 发送请求
    req = urllib2.Request(smsServerUrl, postData)
    response = urllib2.urlopen(req)
    content = response.read()

    # 解析返回结果
    resultCode = int(content)
    if resultCode > 0:
        return {'resultCode': 0, 'resultMessage': '成功'}
    else:
        if resultCode in resultMessage.keys():
            return {'resultCode': resultCode, 'resultMessage': resultMessage[resultCode]}
        else:
            return {'resultCode': -100, 'resultMessage': '未知错误'}


def sendTest(phone, text):
    return {'resultCode': 0, 'resultMessage': '成功'}