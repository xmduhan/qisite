# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.test import TestCase
# Create your models here.


class User(models.Model):
    def __unicode__(self):
        return self.name

    code = models.CharField("用户代码", max_length=50, blank=True)
    phone = models.CharField("手机号码", max_length=50)
    password = models.CharField("密码", max_length=200)
    email = models.CharField("电子邮件", max_length=100, blank=True)
    #Surveys
    #Papers
    #CustLists
    name = models.CharField("姓名", max_length=50, blank=True)
    birthDate = models.DateTimeField("生日", blank=True, null=True)
    #city
    #sex
    #interests
    #education
    #university
    #specialty
    #worktime
    #industry
    #companySize
    #position
    createBy = models.ForeignKey('self', blank=True, null=True, verbose_name="创建者", related_name='userCreated')
    modifyBy = models.ForeignKey('self', blank=True, null=True, verbose_name="修改者", related_name='userModified')
    createTime = models.DateTimeField("创建时间", default=datetime.now)
    modifyTime = models.DateTimeField("修改时间", default=datetime.now)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "[01].用户"
        ordering = ["name"]


class SmsCheckCode(models.Model):
    phone = models.CharField("手机号码", max_length=20)
    checkCode = models.CharField("验证码", max_length=20)
    createTime = models.DateTimeField("创建时间", default=datetime.now)

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = "[02].短信验证码"
        ordering = ["createTime"]


class Test001(TestCase):
    def test001(self):
        pass
