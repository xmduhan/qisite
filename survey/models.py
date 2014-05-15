# -*- coding: utf-8 -*-
from django.db import models
import account.models
from datetime import datetime


class TimeModel(models.Model):
    createTime = models.DateTimeField("创建时间", default=datetime.now())
    modifyTime = models.DateTimeField("修改时间", default=datetime.now())

    class Meta:
        abstract = True


class Paper(TimeModel):
    PAPER_STYLE = ( ('F', 'Flat'), ('P', 'Page'))
    QUESTION_NUM_STYLE = (('S1', 'NUM STYLE 1'), ('S2', 'NUM STYLE 2'), ('S3', 'NUM STYLE 3'))
    title = models.CharField('问卷标题', max_length=500)
    description = models.CharField('问卷说明', max_length=500)
    # 题目集 question_set (ok) (已在Question中设置外键引用)
    inOrder = models.BooleanField('顺序答题')
    QuestionNumStyle = models.CharField('问题标号样式', max_length=50, choices=QUESTION_NUM_STYLE)
    lookBack = models.BooleanField('返回修改')
    style = models.CharField('展现方式', max_length=5, choices=PAPER_STYLE)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='paperCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='paperModified')
    # 样本集 sample_set (ok) (已在sample中设置外键引用)


class PaperCatalog(TimeModel):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    paper_set = models.ManyToManyField(Paper, verbose_name='包含问卷', blank=True, null=True)


class Question(TimeModel):
    QUESTION_TYPE = (('Single', '单选题'), ('Multiple', '多选题'), ('Fillblank', '填空题'), ('Score', '评分题'))
    BRANCH_NUM_STYLE = (('S1', 'NUM STYLE 1'), ('S2', 'NUM STYLE 2'), ('S3', 'NUM STYLE 3'))
    type = models.CharField('题型', max_length=100, choices=QUESTION_TYPE)
    contentLengh = models.IntegerField('内容长度', default=0)  # 仅填空题有效,是否可以作为多选题的选项数量限制
    valueMin = models.FloatField('最小值', null=True, blank=True, default=0)  # 仅评分题有效
    valueMax = models.FloatField('最大值', null=True, blank=True, default=10)  # 仅评分题有效
    # 题干 stem_set 对象集 (ok) (已在stem设置反向外键) 实际没有多个，只是用外键比较方便一些
    # 题支 branch_set 对象集 (ok) (已在branche中设置反向外键)
    confused = models.BooleanField('乱序', default=False)
    branchNumStyle = models.CharField('标号样式', max_length=50, choices=BRANCH_NUM_STYLE)
    nextQuestion = models.ForeignKey('self', verbose_name='下一题', blank=True, null=True)  # 是否需要这个信息,似乎多余?
    paper = models.ForeignKey(Paper, verbose_name='所属问卷', null=True, blank=True)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='questionCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='questionModified')


class QuestionCatalog(TimeModel):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    paper_set = models.ManyToManyField(Question, verbose_name='包含问题')


class Stem(TimeModel):
    text = models.CharField('文字', max_length=300)
    #资源集合 resource_set 对象集 (ok) (已在资源中设置对应外键)
    question = models.ForeignKey(Question, verbose_name="问题")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='stemCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='stemModified')


class Resource(TimeModel):
    resourceType = models.CharField('文字', max_length=50)
    resourceUrl = models.CharField('文字', max_length=1000)
    width = models.FloatField("资源宽度")
    height = models.FloatField("资源高度")
    stem = models.ForeignKey(Stem, verbose_name="对应题干")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='resourceCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='resourceModified')


class Branch(TimeModel):
    text = models.CharField('文字', max_length=200)
    ord = models.IntegerField('排序号')
    nextQuestion = models.ForeignKey(
        # 如何包含结果信息呢？(结束无效问卷,结束有效问卷)
        'Question', verbose_name='下个问题', related_name='fromBranch', null=True, blank=True)
    question = models.ForeignKey(Question, verbose_name="问题")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='branchCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='branchModified')


class Survey(TimeModel):
    paper = models.ForeignKey('Paper', verbose_name="问卷")
    # 目标客户清单 targetcust_set (ok) (已在目标客户中设置外键)
    targetOnly = models.BooleanField('定向调查', default=False)
    state = models.CharField("状态", max_length=5)
    shared = models.BooleanField('是否分享', default=False)
    viewResult = models.BooleanField('查看结果', default=True)
    resubmit = models.BooleanField('是否允许重填', default=True)
    passwd = models.CharField("参与密码", max_length=10, blank=True)
    ipLimit = models.IntegerField("IP限制", default=5)
    macLimit = models.IntegerField("MAC限制", default=5)
    publishTime = models.DateTimeField("发布时间", default=datetime.now())
    endTime = models.DateTimeField("结束时间", default=datetime.now())
    #参与者约束	constraints	对象集 (hold)
    hardCost = models.FloatField('调查费', default=0)
    bonus = models.FloatField('奖金', default=0)
    fee = models.FloatField('手续费', default=0)
    validSampleLimit = models.IntegerField("有效样本上限", default=0)  # 0 表示无限制
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='surveyCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='surveyModified')


class TargetCust(TimeModel):
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('手机号码', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    #自定信息 defineinfo_set 对象集 (ok) (已在DefineInfo中设置对应的外键)
    #sample = models.ForeignKey('Sample', verbose_name='样本') 在样本中已设定了一对一关系 (ok)
    token = models.CharField('访问令牌', max_length=50)
    survey = models.ForeignKey(Survey, verbose_name="所属调查")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='targetCustCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='targetCustModified')


class Sample(TimeModel):
    #样本项集	sampleItems	对象集 (ok) (已在样本中设置对应外键)
    targetCust = models.OneToOneField('TargetCust', verbose_name='清单项', null=True, blank=True)
    user = models.ForeignKey(account.models.User, verbose_name="参与用户", null=True, blank=True)  # 这里是否设置一个related_name
    ipAddress = models.CharField('受访IP', max_length=50)
    macAddress = models.CharField('受访MAC', max_length=50)
    finished = models.BooleanField('是否完成')
    isValid = models.BooleanField('是否完成')
    paper = models.ForeignKey(Paper, verbose_name='所属问卷')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='sampleCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='sampleModified')


class SampleItem(TimeModel):
    question = models.ForeignKey('Question', verbose_name='问题')
    branch_set = models.ManyToManyField(Branch, verbose_name='已选')
    content = models.CharField('内容', max_length=500, blank=True)
    score = models.FloatField('得分')
    sample = models.ForeignKey(Sample, verbose_name='所属样本')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='sampleItemCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='sampleItemModified')


class CustList(TimeModel):
    name = models.CharField('清单名称', max_length=50)
    descrition = models.CharField('清单说明', max_length=200)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='custListCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='custListModified')


class CustListItem(TimeModel):
    name = models.CharField('名称', max_length=50)
    phone = models.CharField('手机号', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    #自定信息	defineInfo	对象集 (ok) (已在DefineInfo中设置对应的外键)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='custListItemCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='custListItemModified')


class DefineInfo(TimeModel):
    name = models.CharField('信息名称', max_length=100)
    value = models.CharField('信息值', max_length=200)
    ord = models.IntegerField('排序号')
    targetCust = models.ForeignKey(TargetCust, verbose_name="所属目标清单")
    custListItem = models.ForeignKey(CustListItem, verbose_name="所属预定清单")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='defineInfoCreated')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='defineInfoModified')