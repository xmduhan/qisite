"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
import json
from services import RESULT_CODE, RESULT_MESSAGE


class DjangoReverseTest(TestCase):
    def setUp(self):
        setup_test_environment()
        self.client = Client()
        self.viewname = 'www:service.django.reverse'
        self.url = reverse(self.viewname)

    def test_no_viewname(self):
        response = self.client.post(self.url, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_VIEWNAME)

    def test_invalid_viewname(self):
        response = self.client.post(self.url, {'viewname': 'just a test'})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.INVALID_VIEWNAME)

    def test_success(self):
        response = self.client.post(self.url, {'viewname': self.viewname})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['url'], self.url)