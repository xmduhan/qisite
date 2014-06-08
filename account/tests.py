#-*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test.client import Client
from django.core.urlresolvers import reverse
from views import SendSmsCheckCode_ErrorMessage, Register_ErrorMessage, Login_ErrorMessage
import json
from time import sleep
from datetime import datetime, timedelta
from models import SmsCheckCode, User
from django.contrib.auth.hashers import make_password, check_password


class SendSmsCheckCodeTest(TestCase):
    '''
        测试发送短信验证码的服务sendSmsCheckCode
    '''

    def test_no_phone(self):
        '''
            测试没有提供手机号码的情况
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:sendSmsCheckCode'),
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], -1)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.no_phone)

    def test_invail_phone(self):
        '''
            测试测试提供无效手机号码的情况
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': '123456'}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], -1)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.invaild_phone)


    def test_success_and_redo(self):
        '''
            测试成功发送和重复发送的情况
        '''
        phone = '18906021980'
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], 0)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.success)

        # 短时间立即做一次
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], -1)
        ##self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.need_wait)
        self.assertTrue(result['secondsRemain'] < 180)
        self.assertTrue(result['secondsRemain'] > 150)
        ## 保存剩余时间提供比较
        secondsRemain = result['secondsRemain']
        ## 保证时间过去1秒可以比较出差别
        sleep(1)

        # 再做第2次
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], -1)
        ## 确认时间是在减少的
        self.assertTrue(result['secondsRemain'] < secondsRemain)

        # 在数据库中尝试寻找记录
        interval = timedelta(minutes=3)
        smsCheckCodeList = SmsCheckCode.objects.filter(
            phone=phone, createTime__gte=datetime.now() - interval
        ).order_by("-createTime")
        self.assertTrue(smsCheckCodeList.count(), 1)


class RegisterTest(TestCase):
    '''
        测试用户注册服务register
    '''

    def test_enter_register_page(self):
        '''
            第1次进入页面的时候，没有提供phone是不会体现错误信息的
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:register'),
        )
        self.assertContains(response, u'<span id="errorMessage"></span>')

    def test_no_phone(self):
        '''
            没有填写phone字段提交时
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:register'), {'phone': ''}
        )
        self.assertContains(response, Register_ErrorMessage.no_phone)

    def test_invaild_phone(self):
        '''
            输入无效的手机号码
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:register'), {'phone': '123456'}
        )
        self.assertContains(response, Register_ErrorMessage.invaild_phone)

    def test_phone_registered(self):
        '''
            测试号码已经注册的情况
        '''
        phone = '18906021980'
        password = 123456
        # 新增一个用户，号码是一个已经注册的手机号
        user = User(phone=phone, password=make_password(password))
        user.save()
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:register'), {'phone': phone}
        )
        self.assertContains(response, Register_ErrorMessage.phone_registered)

    def test_no_check_code(self):
        '''
            测试号码已经注册的情况
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:register'), {'phone': phone}
        )
        self.assertContains(response, Register_ErrorMessage.no_check_code)

    def test_send_check_code_first(self):
        '''
            未发送注册码的情况
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:register'), {'phone': phone, 'checkCode': '123'}
        )
        self.assertContains(response, Register_ErrorMessage.send_check_code_first)

    def test_invaild_check_code(self):
        '''
            注册码不正确的情况
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        # 发送注册码
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], 0)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.success)
        # 提交注册请求
        response = client.post(
            reverse('account:register'), {'phone': phone, 'checkCode': '123'}
        )
        self.assertContains(response, Register_ErrorMessage.invaild_check_code)

    def test_no_password(self):
        '''
            注册码不正确的情况
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        # 发送注册码
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], 0)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.success)
        # 在数据库中找到注册码
        interval = timedelta(minutes=5)
        smsCheckCodeList = SmsCheckCode.objects.filter(
            phone=phone, createTime__gte=datetime.now() - interval
        ).order_by('-createTime')
        # 提交注册请求
        response = client.post(
            reverse('account:register'),
            {'phone': phone, 'checkCode': smsCheckCodeList[0].checkCode}
        )
        self.assertContains(response, Register_ErrorMessage.no_password)


    def test_password_len_lt_6(self):
        '''
            注册码不正确的情况
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        # 发送注册码
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], 0)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.success)
        # 在数据库中找到注册码
        interval = timedelta(minutes=5)
        smsCheckCodeList = SmsCheckCode.objects.filter(
            phone=phone, createTime__gte=datetime.now() - interval
        ).order_by('-createTime')
        # 提交注册请求
        response = client.post(
            reverse('account:register'),
            {'phone': phone, 'checkCode': smsCheckCodeList[0].checkCode, 'password': '123'}
        )
        self.assertContains(response, Register_ErrorMessage.password_len_lt_len6)

    def test_password_different(self):
        '''
            注册码不正确的情况
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        # 发送注册码
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], 0)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.success)
        # 在数据库中找到注册码
        interval = timedelta(minutes=5)
        smsCheckCodeList = SmsCheckCode.objects.filter(
            phone=phone, createTime__gte=datetime.now() - interval
        ).order_by('-createTime')
        # 提交注册请求
        response = client.post(
            reverse('account:register'),
            {'phone': phone, 'checkCode': smsCheckCodeList[0].checkCode, 'password': '123456'}
        )
        self.assertContains(response, Register_ErrorMessage.password_different)

    def test_success(self):
        '''
            测试成功注册
        '''
        phone = '18906021980'
        password = 123456
        setup_test_environment()
        client = Client()
        # 发送注册码
        response = client.post(
            reverse('account:sendSmsCheckCode'),
            {'phone': phone}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], 0)
        self.assertEquals(result['errorMessage'], SendSmsCheckCode_ErrorMessage.success)
        # 在数据库中找到注册码
        interval = timedelta(minutes=5)
        smsCheckCodeList = SmsCheckCode.objects.filter(
            phone=phone, createTime__gte=datetime.now() - interval
        ).order_by('-createTime')
        # 提交注册请求
        client.post(
            reverse('account:register'),
            {'phone': phone,
             'checkCode': smsCheckCodeList[0].checkCode,
             'password': '123456',
             'confirmation': '123456'}
        )
        # 检查数据是否已经添加进去
        userList = User.objects.filter(phone=phone)
        self.assertEquals(userList.count(), 1)


class LoginTest(TestCase):
    '''
        登录页面测试
    '''

    def test_enter_login_page(self):
        '''
            测试首次进入登录页面
        '''
        setup_test_environment()
        client = Client()
        response = client.get(reverse('account:login'))
        self.assertContains(response, u'<span id="errorMessage"></span>')

    def test_no_phone(self):
        '''
            测试没有提供号码的情况
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:login'), {'phone': ''}
        )
        self.assertContains(response, Login_ErrorMessage.no_phone)

    def test_invaild_phone(self):
        '''
            测试提供一个不符规格的手机号码
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:login'), {'phone': '12456789'}
        )
        self.assertContains(response, Login_ErrorMessage.invaild_phone)

    def test_no_password(self):
        '''
            测试提供不提供密码的情况
        '''
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('account:login'), {'phone': '18906021980'}
        )
        self.assertContains(response, Login_ErrorMessage.no_password)

    def test_no_register(self):
        '''
            测试没有注册的情况
        '''
        setup_test_environment()
        # 保证号码没有注册过
        phone = '18906021980'
        User.objects.filter(phone=phone).delete()
        # 测试登录
        client = Client()
        response = client.post(
            reverse('account:login'), {'phone': phone, 'password': '123456'}
        )
        self.assertContains(response, Login_ErrorMessage.no_register)


    def test_phone_or_password_invalid(self):
        '''
            测试错误密码
        '''
        setup_test_environment()
        # 保证号码没有注册过
        phone = '18906021980'
        password = '123456'
        user = User.objects.get_or_create(phone=phone)[0]
        user.password = make_password(password)
        user.save()
        # 测试登录
        client = Client()
        response = client.post(
            reverse('account:login'), {'phone': phone, 'password': '123'}
        )
        self.assertContains(response, Login_ErrorMessage.phone_or_password_invalid)


    def test_success(self):
        '''
            测试成功登录
        '''
        setup_test_environment()
        # 获得测试用户
        phone = '18906021980'
        password = '123456'
        user = User.objects.get_or_create(phone=phone)[0]
        user.password = make_password(password)
        user.save()
        # 测试登录
        client = Client()
        response = client.post(
            reverse('account:login'), {'phone': phone, 'password': password}
        )
        self.assertIn('user', client.session.keys())
        user = client.session['user']
        self.assertEquals(user.phone, phone)
        self.assertTrue(check_password(password, user.password))

