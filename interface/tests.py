# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse
from wechat import TOKEN
import random
import string
from datetime import datetime
import hashlib


class TestWeChat(TestCase):
    def setUp(self):
        #
        setup_test_environment()
        self.url = reverse('interface:wechat')
        self.client = Client()

        # 构造安全验证数据
        self.nonce = "".join(random.sample(string.letters, 10))
        self.timestamp = str(datetime.now())
        keys = [TOKEN, self.timestamp, self.nonce]
        keys.sort()
        self.signature = hashlib.sha1(''.join(keys)).hexdigest()


    def test_interface_create(self):
        '''
            模拟微信服务的开发者验证服务
            具体参见:http://mp.weixin.qq.com/wiki/index.php?title=接入指南
        '''
        echostr = 'hello'
        data = {'signature': self.signature, 'timestamp': self.timestamp, 'nonce': self.nonce, 'echostr': echostr}
        client = self.client
        response = client.get(self.url, data)
        self.assertEquals(echostr, response.content)

    def test_processTextMessage(self):
        '''
            测试从微信公众平台中接收文本消息
        '''
        security = {'signature': self.signature, 'timestamp': self.timestamp, 'nonce': self.nonce}
        message = {'ToUserName': 'ToUserName', 'FromUserName': 'FromUserName', 'CreateTime': 1, 'MsgType': 'text',
                   'Content': 'hello', 'MsgId': 1}
        client = self.client
        client.post(self.url, security, extra=message)


    def test_cheater_request(self):
        pass







