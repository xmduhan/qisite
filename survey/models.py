# -*- coding: utf-8 -*-
from django.db import models
import account.models
# Create your models here.

class Paper(models.Model):
    title = models.CharField('问卷标题', max_length=500)
    description = models.CharField('问卷说明', max_length=500)
    # 题目集 question_set (ok) (已在Question中设置外键引用)
    inOrder = models.BooleanField('顺序答题')
    # 问题标号样式	numStyle 对象 (hold)
    lookBack = models.BooleanField('返回修改')
    style = models.CharField('展现方式', max_length=5)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='paperCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='paperModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")
    # 样本集 samples (ok) (已在sample中设置外键引用)

class PaperCatalog(models.Model):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    # 包含问题 Paper 对象集  多对多 (hold)

class Question(models.Model):
    type = models.CharField('题型',max_length=100)
    contentLengh = models.IntegerField('内容长度')  # 仅填空题有效
    valueMin = models.FloatField('最小值')  # 仅评分题有效
    valueMax = models.FloatField('最大值')
    stem = models.ForeignKey('Stem', verbose_name='题干')
    # 题支 branch_set 对象集 (ok) (已在branche中设置反向外键)
    confused = models.BooleanField('乱序')
    #题支编号样式	numStyle  对象 (hold)
    nextQuestion = models.ForeignKey('self', verbose_name='下一题')
    paper = models.ForeignKey(Paper,verbose_name='所属问卷')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='questionCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='questionModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class QuestionCatalog(models.Model):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    # 包含问题 questions 对象集 多对多 (hold)

class Stem(models.Model):
    text = models.CharField('文字',max_length=300)
    #资源集合 resource_set 对象集 (ok) (已在资源中设置对应外键)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='stemCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='stemModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class Resource(models.Model):
    resourceType = models.CharField('文字',max_length=50)
    resourceUrl = models.CharField('文字',max_length=1000)
    width = models.FloatField("资源宽度")
    height = models.FloatField("资源高度")
    stem = models.ForeignKey(Stem, verbose_name="对应题干")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='resourceCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='resourceModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class Branch(models.Model):
    text = models.CharField('文字',max_length=200)
    ord = models.IntegerField('排序号')
    nextQuestion = models.ForeignKey('Question', verbose_name='下个问题',related_name='fromBranch')
    question =  models.ForeignKey(Question, verbose_name="问题")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='branchCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='branchModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class Survey(models.Model):
    paper = models.ForeignKey('Paper', verbose_name="问卷")
    # 目标客户清单 targetcust_set (ok) (已在目标客户中设置外键)
    targetOnly = models.BooleanField('定向调查')
    state = models.CharField("状态", max_length=5)
    shared = models.BooleanField('是否分享')
    viewResult = models.BooleanField('查看结果')
    resubmit = models.BooleanField('是否允许重填')
    passwd = models.CharField("参与密码", max_length=5)
    ipLimit = models.IntegerField("IP限制")
    macLimit = models.IntegerField("MAC限制")
    publishTime = models.DateTimeField("发布时间")
    endTime = models.DateTimeField("结束时间")
    #参与者约束	constraints	对象集 (hold)
    hardCost = models.FloatField('调查费')
    bonus = models.FloatField('奖金')
    fee = models.FloatField('手续费')
    validSampleLimit = models.IntegerField("有效样本上限")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='surveyCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='surveyModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class TargetCust(models.Model):
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('手机号码', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    #自定信息 defineinfo_set 对象集 (ok) (已在DefineInfo中设置对应的外键)
    #sample = models.ForeignKey('Sample', verbose_name='样本') 在样本中已设定了一对一关系 (ok)
    token = models.CharField('访问令牌', max_length=50)
    survey = models.ForeignKey(Survey, verbose_name="所属调查")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='targetCustCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='targetCustModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class Sample(models.Model):
    #样本项集	sampleItems	对象集 (ok) (已在样本中设置对应外键)
    targetCust = models.OneToOneField('TargetCust', verbose_name='清单项')
    user = models.ForeignKey(account.models.User, verbose_name="参与用户")  # 这里是否设置一个related_name
    ipAddress = models.CharField('受访IP', max_length=50)
    macAddress = models.CharField('受访MAC', max_length=50)
    finished = models.BooleanField('是否完成')
    isValid = models.BooleanField('是否完成')
    paper = models.ForeignKey(Paper,verbose_name='所属问卷')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='sampleCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='sampleModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class SampleItem(models.Model):
    question = models.ForeignKey('Question', verbose_name='问题')
    # 已选项 branches 对象集  多对多关系 (hold)
    content = models.CharField('内容', max_length=500)
    score = models.FloatField('得分')
    sample = models.ForeignKey(Sample,verbose_name='所属样本')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='sampleItemCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='sampleItemModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class CustList(models.Model):
    name = models.CharField('清单名称', max_length=50)
    descrition = models.CharField('清单说明', max_length=200)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='custListCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='custListModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class CustListItem(models.Model):
    name = models.CharField('名称',max_length=50)
    phone = models.CharField('手机号', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    #自定信息	defineInfo	对象集 (ok) (已在DefineInfo中设置对应的外键)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='custListItemCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='custListItemModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

class DefineInfo(models.Model):
    name = models.CharField('信息名称', max_length=100)
    value = models.CharField('信息值', max_length=200)
    ord = models.IntegerField('排序号')
    targetCust = models.ForeignKey(TargetCust, verbose_name="所属目标清单")
    custListItem = models.ForeignKey(CustListItem, verbose_name="所属预定清单")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者",related_name='defineInfoCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",related_name='defineInfoModified')
    createTime = models.DateTimeField("创建时间")
    modifyTime = models.DateTimeField("修改时间")

