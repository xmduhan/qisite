# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import format_html
# Create your models here.


'''
（一）模型设计存在的问题
1、对象数据历史记录问题
2、图像数据保存问题
3、每种对象的文本名称，用了不同的名称造成混乱
4、ord可以做到抽象类中
5、如果单从存储对象是否被删除的信息来说，state字段是否有存在的必要，是否可以用历史表方式来存储
6、存储用户所答问卷信息，是否有必要存储UserQuestion对象，实际存储UserChoice就可以还原
7、用户的问卷信息压根就不能用admin来管理不是一路东西(admin不能解决一切问题,admin顶多管理好配置数据)


（二）可能需要开发的界面
1、树状结构显示出以完整的目录配置情况
lv1>lv2>lv3
<form  -----------------------------------------------
       -----------------------------------------------
       -----------------------------------------------
       -----------------------------------------------
       -----------------------------------------------
/form>
2、模拟答题界面


3、展示答题结果的界面
'''


class StateObject(models.Model):
    stateChoices = (('A', '在用'), ('P', '删除'))
    create_date = models.DateTimeField("创建时间")
    modify_date = models.DateTimeField("修改时间")
    state = models.CharField("状态", max_length=5, choices=stateChoices)

    class Meta:
        abstract = True;


class Paper(StateObject):
    def __unicode__(self):
        return self.name

    name = models.CharField("问卷名称", max_length=500)
    description = models.CharField("问卷说明", max_length=1000)

    class Meta:
        verbose_name = "问卷"
        verbose_name_plural = "<03>.问卷"
        ordering = ["name"]


class Catalog(StateObject):
    def __unicode__(self):
        return self.name

    name = models.CharField("目录名称", max_length=500)
    code = models.CharField("目录编码", max_length=50, unique=True)
    # image = models.ImageField(blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="上级目录");
    ord = models.IntegerField("排序号")
    # ord1 = models.IntegerField("排序号1", blank=True, null=True)
    papers = models.ManyToManyField(Paper, through='CatalogPaper', verbose_name="包含问卷")

    class Meta:
        verbose_name = "目录"
        verbose_name_plural = "<01>.目录"


class CatalogPaper(StateObject):
    catalog = models.ForeignKey(Catalog, verbose_name="目录")
    paper = models.ForeignKey(Paper, verbose_name="问卷")
    ord = models.IntegerField("排序号")

    def __unicode__(self):
        return self.catalog.name + "(" + self.catalog.code + ")/" + self.paper.name

    def getCatalogCode(self):
        # return self.catalog.code
        return format_html('<span style="color: {0};">{1}</span>', "blue", self.catalog.code)

    getCatalogCode.allow_tags = True
    getCatalogCode.short_description = "目录编码"

    class Meta:
        verbose_name = "目录-问卷"
        verbose_name_plural = "<02>.目录-问卷"
        ordering = ["ord"]


class QuestionType(StateObject):
    def __unicode__(self):
        return self.name

    code = models.CharField("类型代码", max_length=50)
    name = models.CharField("类型名称", max_length=200)
    description = models.CharField("描述", max_length=500)
    ord = models.IntegerField("排序号")

    class Meta:
        verbose_name = "问题类型"
        verbose_name_plural = "<05>.问题类型"
        ordering = ["ord"]


class Question(StateObject):
    def __unicode__(self):
        return self.title

    code = models.CharField("代码", max_length=50)
    title = models.CharField("标题", max_length=500)
    type = models.ForeignKey(QuestionType, verbose_name="问题类型")
    paper = models.ForeignKey(Paper, verbose_name="问卷")
    ord = models.IntegerField("排序号")

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = "<04>.问题"
        ordering = ["ord"]


class ChoiceType(StateObject):
    def __unicode__(self):
        return self.name

    code = models.CharField("类型代码", max_length=50)
    name = models.CharField("类型名称", max_length=200)
    description = models.CharField("描述", max_length=500);
    ord = models.IntegerField("排序号");

    class Meta:
        verbose_name = "选项类型"
        verbose_name_plural = "<06>.选项类型"
        ordering = ["ord"]


class Choice(StateObject):
    def __unicode__(self):
        return self.text

    code = models.CharField("代码", max_length=50)
    text = models.CharField("内容", max_length=500)
    type = models.ForeignKey(ChoiceType, verbose_name="选项类型")
    question = models.ForeignKey(Question, verbose_name="问题")
    ord = models.IntegerField("排序号")

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = "<05>.选项"
        ordering = ["ord"]


class User(StateObject):
    def __unicode__(self):
        return self.name + "(" + self.phone + ")"

    phone = models.CharField("手机号码", max_length=50)
    name = models.CharField("用户名", max_length=50)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "<07>.用户"
        ordering = ["phone"]


class UserPaper(StateObject):  # 应该UserPaper/UserQuestion/UserChoice  做成三级主从
    def __unicode__(self):
        return self.user.name + "(" + self.user.phone + ")" + self.paper.name

    user = models.ForeignKey(User, verbose_name="用户")
    paper = models.ForeignKey(Paper, verbose_name="问卷")

    class Meta:
        verbose_name = "用户-问卷"
        verbose_name_plural = "<08>.用户-问卷"


class UserQuestion(StateObject):
    def __unicode__(self):
        return self.userpaper.__unicode__() + "--" + self.question.title

    userpaper = models.ForeignKey(UserPaper, verbose_name="用户问卷")
    question = models.ForeignKey(Question, verbose_name="问题")
    ord = models.IntegerField("排序号")

    class Meta:
        verbose_name = "用户-问题"
        verbose_name_plural = "<09>.用户-问题"


class UserChoice(StateObject):  #  考虑此类是否要和UserQuestion关联,而不要直接和User关联
    def __unicode__(self):
        return self.userquestion.__unicode__() + "--" + self.choice.text

    userquestion = models.ForeignKey(UserQuestion, verbose_name="用户问题")
    choice = models.ForeignKey(Choice, verbose_name="选项")
    text = models.CharField("附加文本", max_length=200)
    grade = models.IntegerField("附加评分");
    ord = models.IntegerField("排序号", blank=True, null=True)

    class Meta:
        verbose_name = "用户-选项"
        verbose_name_plural = "<10>.用户-选项"





