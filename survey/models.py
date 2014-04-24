# -*- coding: utf-8 -*-
from django.db import models
import account.models
# Create your models here.



class PaperCatalog(models.Model):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    # 包含问题 Paper 对象集


class Survey(models.Model):
    paper =	models.ForeignKey(Paper, verbose_name="问卷")
    #targetCusts	= models.OneToManyField(TargetCust,verbose_name="清单")
    targetOnly	= models.BooleanField('定向调查')
    state	    =  models.CharField("状态", max_length=5)
    shared	= models.BooleanField('是否分享')
    viewResult = models.BooleanField('查看结果')
    resubmit	= models.BooleanField('是否允许重填')
    passwd	=models.CharField("参与密码", max_length=5)
    ipLimit	= models.IntegerField("IP限制")
    macLimit = models.IntegerField("MAC限制")
    publishTime	= models.DateTimeField("发布时间")
    endTime	= models.DateTimeField("结束时间")
    #参与者约束	constraints	对象集
    hardCost = models.FloatField('调查费')
    bonus = models.FloatField('奖金')
    fee	= models.FloatField('手续费')
    validSampleLimit = models.IntegerField("有效样本上限")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class TargetCust(models.Model):
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('手机号码', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    #自定信息	defineInfo	对象集
    sample = models.ForeignKey(Sample,'样本')
    token = models.CharField('访问令牌',max_length=50)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")
    survey = models.ForeignKey(Survey, verbose_name="问卷")

class Paper(models.Model):
    title = models.CharField('问卷标题', max_length=500)
    description = models.CharField('问卷说明', max_length=500)
    # 题目集	questions
    inOrder	= models.BooleanField('顺序答题')
    # 问题标号样式	numStyle	对象
    lookBack=models.BooleanField('返回修改')
    style=models.CharField('展现方式')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class QuestionCatalog(models.Model):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    # 包含问题 questions 对象集


class Question(models.Model):
    type=models.CharField('题型')
    contentLengh = models.IntegerField('内容长度') # 仅填空题有效
    valueMin = models.FloatField('最小值')  # 仅评分题有效
    valueMax =  models.FloatField('最大值')
    stem = models.ForeignKey(Stem,'题干')
    # 题支	branches	对象集
    confused = models.BooleanField('乱序')
    #题支编号样式	numStyle	对象
    nextQuestion = models.ForeignKey('self','下一题')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")


class Stem(models.Model):
    text = models.CharField('文字')
    #资源集合	resources	对象集
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")


class Branch(models.Model):
    text = models.CharField('文字')
    ord = models.IntegerField('排序号')
    nextQuestion = models.ForeignKey(Question,'下个问题')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")


class Sample(models.Model):
    #样本项集	sampleItems	对象集
    targetCust = models.ForeignKey(TargetCust,'清单项')
    user = models.ForeignKey(account.models.User, verbose_name="用户")
    ipAddress = models.CharField('受访IP',max_length=50)
    macAddress = models.CharField('受访MAC',max_length=50)
    finished = models.BooleanField('是否完成')
    isValid	= models.BooleanField('是否完成')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")


class SampleItem(models.Model):
    question = models.ForeignKey(Question,'问题')
    # 已选项	branches 对象集
    content = models.CharField('内容',max_length=500)
    score = models.FloatField('得分')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")


class CustList(models.Model):
    name = models.CharField('清单名称',max_length=50)
    descrition = models.CharField('清单说明',max_length=200)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class CustListItem(models.Model):
    name = models.CharField('名称')
    phone = models.CharField('手机号',max_length=50)
    email = models.CharField('电子邮件',max_length=100)
    #自定信息	defineInfo	对象集
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")


class DefineInfo(models.Model):
    name = models.CharField('信息名称',max_length = 100)
    value = models.CharField('信息值',max_length = 200)
    ord = models.IntegerField('排序号')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者")
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者")
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")