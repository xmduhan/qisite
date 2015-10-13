#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from models import Paper
from account.models import User
from django.core.urlresolvers import reverse
from account.tests import loginForTest


class PaperPreviewTest(TestCase):
    """
    问卷预览测试
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        """
        准备数据
        """
        setup_test_environment()
        self.client = Client()
        self.paper = Paper.objects.get(code='paper-template-01', type='T')  # 网购客户满意度调查(非定向)
        self.previewUrl = reverse('survey:view.paper.preview', args=[self.paper.id])

        self.user = User.objects.get(code='duhan')
        loginForTest(self.client, self.user.phone, '123456')

    def test_preview_simple_paper(self):
        """
        测试是否能正常生成预览页面
        """
        response = self.client.get(self.previewUrl)
        self.assertEqual(response.status_code, 302)
        redirectUrl = response._headers['location'][1]
        response = self.client.get(redirectUrl)
        self.assertEqual(response.status_code, 200)
