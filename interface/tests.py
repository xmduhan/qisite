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
        setup_test_environment()
        self.url = reverse('interface:wechat')
        self.client = Client()


    def test_interface_create(self):
        '''
            模拟微信服务的开发者验证服务
            具体参见:http://mp.weixin.qq.com/wiki/index.php?title=接入指南
        '''
        echostr = 'hello'
        nonce = "".join(random.sample(string.letters, 10))
        timestamp = str(datetime.now())
        signature = hashlib.sha1(''.join([TOKEN, timestamp, nonce])).hexdigest()
        data = {'signature': signature, 'timestamp': timestamp, 'nonce': nonce, 'echostr': echostr}
        client = self.client
        response = client.get(self.url, data)
        self.assertEquals(echostr, response.content)






