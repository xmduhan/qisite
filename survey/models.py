# -*- coding: utf-8 -*-
from django.db import models
import account.models
from datetime import datetime
from numstyle import NumStyle, defaultQuestionNumStyle, defaultBranchNumStyle
from django.core.exceptions import ValidationError
from django.core.signing import Signer


class TimeModel(models.Model):
    createTime = models.DateTimeField("创建时间", default=datetime.now)
    modifyTime = models.DateTimeField("修改时间", default=datetime.now)

    class Meta:
        abstract = True


class Paper(TimeModel):
    def __unicode__(self):
        return self.title

    #PAPER_STYLE = ( ('F', '平展'), ('P', '分页'))
    QUESTION_NUM_STYLE = (('123', '1.2.3.……'), ('(1)(2)(3)', '(1).(2).(3).……'), ('Q1Q2Q3', 'Q1.Q2.Q3.……'))
    title = models.CharField('问卷标题', max_length=500)
    description = models.CharField('问卷说明', max_length=500, blank=True)
    # 题目集 question_set (ok) (已在Question中设置外键引用)
    inOrder = models.BooleanField('顺序答题', default=False)
    questionNumStyle = models.CharField(
        '问题标号样式', max_length=50, choices=QUESTION_NUM_STYLE, default=defaultQuestionNumStyle)
    lookBack = models.BooleanField('返回修改', default=False)
    #style = models.CharField('展现方式', max_length=5, choices=PAPER_STYLE) #使用paging字段取代
    paging = models.BooleanField('分页答题', default=True)
    createBy = models.ForeignKey(
        account.models.User, verbose_name="创建者", related_name='paperCreated_set', blank=True, null=True)
    modifyBy = models.ForeignKey(
        account.models.User, verbose_name="修改者", related_name='paperModified_set', blank=True, null=True)
    # 样本集 sample_set (ok) (已在sample中设置外键引用)
    def clean(self):
        '''
            说明：
            1、createBy和modifyBy不能为空的校验放在这里，主要是考虑到我们经常需要创建一些测试用的Paper，如果这两个字段在
            定义时就限定死成不能为空，则每次我们都还要多创建一个User，比较麻烦。
        '''
        if self.createBy is None:
            raise ValidationError(u'创建者信息不能为空')
        if self.modifyBy is None:
            raise ValidationError(u'修改者信息不能为空')

    class Meta:
        verbose_name = "问卷"
        verbose_name_plural = "[01].问卷"
        ordering = ["title"]

    def getQuestionSetInOrder(self):
        return self.question_set.order_by('ord')

    def getNumStyleAvailable(self):
        return Paper.QUESTION_NUM_STYLE

    def getIdSigned(self):
        signer = Signer()
        return signer.sign(self.id)


class PaperCatalog(TimeModel):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', verbose_name="上级目录", blank=True, null=True)
    ord = models.IntegerField("排序号")
    paper_set = models.ManyToManyField(Paper, verbose_name='包含问卷', through='PaperCatalogPaper')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='paperCatalogCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='paperCatalogModified_set')

    class Meta:
        verbose_name = "问卷目录"
        verbose_name_plural = "[02].问卷目录"


class PaperCatalogPaper(TimeModel):
    paperCatalog = models.ForeignKey(PaperCatalog, verbose_name='对应的目录')
    paper = models.ForeignKey(Paper, verbose_name='对应的问卷')
    ord = models.IntegerField("排序号")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='paperCatalogPaperCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='paperCatalogPaperModified_set')

    class Meta:
        verbose_name = "问卷目录-问卷"
        verbose_name_plural = "[03].问卷目录-问卷"


class Question(TimeModel):
    QUESTION_TYPE = (
        ('Single', '单选题'), ('Multiple', '多选题'), ('Fillblank', '填空题'), ('Score', '评分题'),
        ('EndValid', '有效结束'), ('EndInvalid', '无效结束')
    )
    QUESTION_TYPE_AVAILABLE = ('Single', 'Multiple', 'Fillblank', 'Score')
    BRANCH_NUM_STYLE = (('ABC', 'A.B.C.……'), ('abc.', 'a.b.c.……'), ('123.', '1.2.3……'))
    text = models.CharField('文字', max_length=300)
    type = models.CharField('题型', max_length=100, choices=QUESTION_TYPE)
    ord = models.IntegerField("排序号")
    contentLength = models.IntegerField('内容长度', default=0)  # 仅填空题有效,是否可以作为多选题的选项数量限制
    valueMin = models.FloatField('最小值', null=True, blank=True, default=0)  # 仅评分题有效
    valueMax = models.FloatField('最大值', null=True, blank=True, default=10)  # 仅评分题有效
    # 题支 branch_set 对象集 (ok) (已在branche中设置反向外键)
    confused = models.BooleanField('乱序', default=False)
    branchNumStyle = models.CharField('标号样式', max_length=50, choices=BRANCH_NUM_STYLE, default=defaultBranchNumStyle)
    nextQuestion = models.ForeignKey('self', verbose_name='下一题', blank=True, null=True)  # 是否需要这个信息,似乎多余?
    paper = models.ForeignKey(Paper, verbose_name='所属问卷', null=True, blank=True)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='questionCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='questionModified_set')

    def clean(self):
        '''
            问题模型校验
        '''
        if self.type not in Question.QUESTION_TYPE_AVAILABLE:
            raise ValidationError(u'无效的问题类型')
        if self.type in ( 'Single', 'Multiple') and self.contentLength != 0:
            raise ValidationError(u'选择题不能有填写值长度')
        if self.type not in ( 'Single', 'Multiple') and self.confused:
            raise ValidationError(u'非选择题不能指定乱序选项')

    def getStemText(self):
        '''
            通过问题直接读取题干的文字信息
        '''
        return self.text

    getStemText.short_description = '题干信息'

    def getBranchSetInOrder(self):
        return self.branch_set.order_by('ord')

    def getNum(self):
        # 针对特殊问题类型做特殊处理
        if self.type in ('EndValid', 'EndInvalid'):
            return self.get_type_display()
        else:
            numStyle = NumStyle(self.paper.questionNumStyle)
            return numStyle.getNum(self.ord)

    def __unicode__(self):
        return u"(%d)(%s)%s" % (self.ord, self.type, unicode(self.text))

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = "[04].问题"
        ordering = ["ord"]

    def getIdSigned(self):
        signer = Signer()
        return signer.sign(self.id)


class QuestionCatalog(TimeModel):
    name = models.CharField("目录名称", max_length=100)
    code = models.CharField("目录编码", max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录")
    ord = models.IntegerField("排序号")
    question_set = models.ManyToManyField(Question, verbose_name='包含问题', through='QuestionCatalogQuestion')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='questionCatalogCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者",
                                 related_name='questionCatalogModified_set')

    class Meta:
        verbose_name = "问题目录"
        verbose_name_plural = "[05].问题目录"


class QuestionCatalogQuestion(TimeModel):
    questionCatalog = models.ForeignKey(QuestionCatalog, verbose_name='对应的目录')
    question = models.ForeignKey(Question, verbose_name='对应的问题')
    ord = models.IntegerField("排序号")
    createBy = models.ForeignKey(
        account.models.User, verbose_name="创建者", related_name='questionCatalogQuestionCreated_set')
    modifyBy = models.ForeignKey(
        account.models.User, verbose_name="修改者", related_name='questionCatalogQuestionModified_set')

    class Meta:
        verbose_name = "问题目录-问题"
        verbose_name_plural = "[06].问题目录-问题"


class Resource(TimeModel):
    RESOURCE_TYPE = (('Picture', '图片'), ('Audio', '音频'), ('Video', '视频'))
    resourceType = models.CharField('文字', max_length=50, choices=RESOURCE_TYPE)
    resourceUrl = models.CharField('文字', max_length=1000)
    width = models.FloatField("资源宽度")
    height = models.FloatField("资源高度")
    question = models.ForeignKey(Question, verbose_name="对应问题")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='resourceCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='resourceModified_set')

    class Meta:
        verbose_name = "资源"
        verbose_name_plural = "[08].资源"


class Branch(TimeModel):
    text = models.CharField('文字', max_length=200)
    ord = models.IntegerField('排序号')
    nextQuestion = models.ForeignKey(
        # 如何包含结果信息呢？(结束无效问卷,结束有效问卷)
        'Question', verbose_name='下个问题', related_name='fromBranch', null=True, blank=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, verbose_name="问题")
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='branchCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='branchModified_set')

    class Meta:
        verbose_name = "题支"
        verbose_name_plural = "[09].题支"

    def getNum(self):
        numStyle = NumStyle(self.question.branchNumStyle)
        return numStyle.getNum(self.ord)

    def getReachableQuestionList(self):
        # 获取当前选项对应问题的之后的所有问题
        question = self.question
        paper = question.paper
        reachableQuestion = list(paper.question_set.filter(ord__gt=question.ord).order_by('ord'))
        return reachableQuestion

    def getSystemPredefined(self):
        # 获取预定义的问题
        systemPredefinedCatalog = QuestionCatalog.objects.filter(code='SystemPredefined')[0]
        systemPredefined = list(systemPredefinedCatalog.question_set.order_by('ord'))
        return systemPredefined

    def getIdSigned(self):
        signer = Signer()
        return signer.sign(self.id)


class Survey(TimeModel):
    paper = models.ForeignKey('Paper', verbose_name="问卷", null=True, blank=True, on_delete=models.SET_NULL)
    # 目标客户清单 targetcust_set (ok) (已在目标客户中设置外键)
    targetOnly = models.BooleanField('定向调查', default=False)
    state = models.CharField("状态", max_length=5)
    shared = models.BooleanField('是否分享', default=False)
    viewResult = models.BooleanField('查看结果', default=True)
    resubmit = models.BooleanField('是否允许重填', default=True)
    password = models.CharField("参与密码", max_length=10, blank=True)
    ipLimit = models.IntegerField("IP限制", default=5)
    macLimit = models.IntegerField("MAC限制", default=5)
    publishTime = models.DateTimeField("发布时间", default=datetime.now)
    endTime = models.DateTimeField("结束时间", default=datetime.now)
    #参与者约束	constraints	对象集 (hold)
    hardCost = models.FloatField('调查费', default=0)
    bonus = models.FloatField('奖金', default=0)
    fee = models.FloatField('手续费', default=0)
    validSampleLimit = models.IntegerField("有效样本上限", default=0)  # 0 表示无限制
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='surveyCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='surveyModified_set')

    class Meta:
        verbose_name = "调查"
        verbose_name_plural = "[10].调查"


class TargetCust(TimeModel):
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('手机号码', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    defineInfo_set = models.ManyToManyField('DefineInfo', verbose_name='附件信息')
    #sample = models.ForeignKey('Sample', verbose_name='样本') 在样本中已设定了一对一关系 (ok)
    token = models.CharField('访问令牌', max_length=50)
    survey = models.ForeignKey(Survey, verbose_name="所属调查", related_name='targetCust_set')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='targetCustCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='targetCustModified_set')

    class Meta:
        verbose_name = "目标客户"
        verbose_name_plural = "[11].目标客户"


class Sample(TimeModel):
    #样本项集	sampleItems	对象集 (ok) (已在样本中设置对应外键)
    targetCust = models.OneToOneField('TargetCust', verbose_name='清单项', null=True, blank=True)
    user = models.ForeignKey(account.models.User, verbose_name="参与用户", null=True,
                             blank=True)  # 这里是否设置一个related_name
    ipAddress = models.CharField('受访IP', max_length=50)
    macAddress = models.CharField('受访MAC', max_length=50)
    finished = models.BooleanField('是否完成')
    isValid = models.BooleanField('是否完成')
    paper = models.ForeignKey(Paper, verbose_name='所属问卷')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='sampleCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='sampleModified_set')

    class Meta:
        verbose_name = "样本"
        verbose_name_plural = "[12].样本"


class SampleItem(TimeModel):
    question = models.ForeignKey('Question', verbose_name='问题')
    branch_set = models.ManyToManyField(Branch, verbose_name='已选')
    content = models.CharField('内容', max_length=500, blank=True, null=True)
    score = models.FloatField('得分', default=0)
    sample = models.ForeignKey(Sample, verbose_name='所属样本')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='sampleItemCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='sampleItemModified_set')

    class Meta:
        verbose_name = "样本项"
        verbose_name_plural = "[13].样本项"


class CustList(TimeModel):
    name = models.CharField('清单名称', max_length=50)
    descrition = models.CharField('清单说明', max_length=200)
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='custListCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='custListModified_set')

    class Meta:
        verbose_name = "客户清单"
        verbose_name_plural = "[14].客户清单"


class CustListItem(TimeModel):
    name = models.CharField('名称', max_length=50)
    phone = models.CharField('手机号', max_length=50)
    email = models.CharField('电子邮件', max_length=100)
    custList = models.ForeignKey(CustList, verbose_name='所属清单', related_name="custListItem_set")
    defineInfo_set = models.ManyToManyField('DefineInfo', verbose_name='附件信息')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='custListItemCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='custListItemModified_set')

    class Meta:
        verbose_name = "客户清单项"
        verbose_name_plural = "[15].客户清单项"


class DefineInfo(TimeModel):
    name = models.CharField('信息名称', max_length=100)
    value = models.CharField('信息值', max_length=200)
    ord = models.IntegerField('排序号')
    createBy = models.ForeignKey(account.models.User, verbose_name="创建者", related_name='defineInfoCreated_set')
    modifyBy = models.ForeignKey(account.models.User, verbose_name="修改者", related_name='defineInfoModified_set')

    class Meta:
        verbose_name = "自定义信息"
        verbose_name_plural = "[16].自定义信息"


