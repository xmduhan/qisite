#-*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test.client import Client
from django.core.urlresolvers import reverse
from views import SendSmsCheckCode_ErrorMessage
import json


class sendSmsCheckCodeTest(TestCase):
    '''
        测试发送短信验证码的服务sendSmsCheckCode
    '''

    def test_invail_phone(self):
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': '123456'}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], -1)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.invaild_phone)


