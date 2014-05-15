# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
import account.models
from datetime import datetime


class SurveyModelTest(TestCase):
    def addUser(self):
        user = account.models.User(name='tsUser', phone='1234567890', email='sample@example.com')
        user.save()
        self.tsUser = user

    def addPaper(self):
        paper = Paper(
            title='tsPaper', description='tsPaper.description', inOrder=True, lookBack=False, style='P',
            createBy=self.tsUser, modifyBy=self.tsUser
        )
        paper.save()
        self.tsPaper = paper

    def addSurvey(self):
        survey = Survey(
            paper=self.tsPaper,  # 在没有问卷的情况下，是无法创建调查的
            targetOnly=True, state='?', shared=False, viewResult=False, resubmit=False, passwd='',
            hardCost=0, bonus=0, fee=0, validSampleLimit=0, createBy=self.tsUser, modifyBy=self.tsUser
            #survey.ipLimit = 5  #survey.ipLimit = 5  # 用来测试默认值
        )
        survey.save()
        self.tsSurvey = survey

    def addSingleQuestion(self):
        # 增加一个单选题
        singleQuestion = Question(
            type='Single', contentLengh=0, valueMin=0, valueMax=0, confused=False, branchNumStyle='S1',
            nextQuestion=None, paper=self.tsPaper, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleQuestion.save()
        self.tsSingleQuestion = singleQuestion
        # 增加单选题的题干
        singleStem = Stem(text='选择题', question=singleQuestion, createBy=self.tsUser, modifyBy=self.tsUser)
        singleStem.save()
        self.tsSingleStem = singleStem
        # 增加题干的资源
        singleResource = Resource(
            resourceType='Picture', resourceUrl='http://example.com/picture/111', width=640, height=480,
            stem=singleStem, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleResource.save()
        self.singleResource = singleResource
        # 增加题支
        ## 1
        singleBranch1 = Branch(
            text='选项1', ord=1, nextQuestion=None, question=singleQuestion, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleBranch1.save()
        self.tsSingleBranch1 = singleBranch1
        ## 2
        singleBranch2 = Branch(
            text='选项2', ord=2, nextQuestion=None, question=singleQuestion, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleBranch2.save()
        self.tsSingleBranch2 = singleBranch2
        ## 3
        singleBranch3 = Branch(
            text='选项3', ord=3, nextQuestion=None, question=singleQuestion, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleBranch3.save()
        self.tsSingleBranch3 = singleBranch3
        ## 4
        singleBranch4 = Branch(
            text='选项4', ord=4, nextQuestion=None, question=singleQuestion, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleBranch4.save()
        self.tsSingleBranch4 = singleBranch4

    def addQuestions(self):
        self.addSingleQuestion()

    def addTargetCust(self):
        # 添加附件清单项
        targetCust = TargetCust(
            name='用户1', phone='1234567890', email='targetCust@example.com', token='XC65GXAG',
            survey=self.tsSurvey, createBy=self.tsUser, modifyBy=self.tsUser
        )
        targetCust.save()
        self.tsTargetCust = targetCust
        # 添加附件清单的附加信息
        # 1
        targetCustInfo1 = DefineInfo(
            name='附件信息1', value='附件信息1-内容', ord=0, createBy=self.tsUser, modifyBy=self.tsUser
        )
        targetCustInfo1.save()
        targetCust.defineinfo_set.add(targetCustInfo1)
        targetCust.save()
        # 2
        targetCustInfo2 = DefineInfo(
            name='附件信息2', value='附件信息2-内容', ord=1, createBy=self.tsUser, modifyBy=self.tsUser
        )
        targetCustInfo2.save()
        targetCust.defineinfo_set.add(targetCustInfo2)
        targetCust.save()

    def addSamples(self):
        #  添加样本
        sample = Sample(
            targetCust=self.tsTargetCust, user=None, ipAddress='127.0.0.1', macAddress='B8-70-F4-13-43-C6',
            finished=True, isValid=True, paper=self.tsPaper, createBy=self.tsUser, modifyBy=self.tsUser
        )
        sample.save()
        #  添加样本项
        sampleItem = SampleItem(
            question=self.tsSingleQuestion, content=None, score=0, sample=sample, createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        sampleItem.save()
        sampleItem.branch_set.add(self.tsSingleBranch3)
        sampleItem.save()

    def addPaperCatalog(self):
        paperCatalog = PaperCatalog(
            name='测试问卷目录', code='TestPaperCatalog', parent=None, ord=0, createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        paperCatalog.save()
        paperCatalog.paper_set.add(self.tsPaper)
        paperCatalog.save()


    def addQuestionCatalog(self):
        questionCatalog = QuestionCatalog(
            name='测试问题目录', code='TestQestionCatalog', parent=None, ord=0, createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        questionCatalog.save()
        questionCatalog.question_set.add(self.tsSingleQuestion)
        questionCatalog.save()

    def addCustList(self):
        # 添加清单(帽子)
        custList = CustList(name='客户清单', descrition='2013年发展', createBy=self.tsUser, modifyBy=self.tsUser)
        custList.save()
        self.tsCustList = custList
        # 添加清单项
        # 1
        custListItem1 = CustListItem(
            name='客户1', phone='1234567890-1', email='cust1@example.com', custList=custList,
            createBy=self.tsUser, modifyBy=self.tsUser
        )
        custListItem1.save()
        self.tsCustListItem1 = custListItem1
        ## 增加附件信息 1
        custListItemInfo1 = DefineInfo(
            name='购买产品类型', value='型号1', ord=0, createBy=self.tsUser, modifyBy=self.tsUser
        )
        custListItemInfo1.save()
        self.tsCustListItemInfo1 = custListItemInfo1
        custListItem1.defineinfo_set.add(custListItemInfo1)
        custListItem1.save()
        # 2
        custListItem2 = CustListItem(
            name='客户2', phone='1234567890-2', email='cust2@example.com', custList=custList,
            createBy=self.tsUser, modifyBy=self.tsUser
        )
        custListItem2.save()
        self.tsCustListItem2 = custListItem2
        ## 增加附件信息 2
        custListItemInfo2 = DefineInfo(
            name='购买产品类型', value='型号2', ord=0, createBy=self.tsUser, modifyBy=self.tsUser
        )
        custListItemInfo2.save()
        self.tsCustListItemInfo2 = custListItemInfo2
        custListItem2.defineinfo_set.add(custListItemInfo2)
        custListItem2.save()

    ''' 目前还不在测试数据中的实体
    DefineInfo
    '''

    def setUp(self):
        self.addUser()
        self.addPaper()
        self.addSurvey()
        self.addQuestions()
        self.addTargetCust()
        self.addSamples()
        self.addPaperCatalog()
        self.addQuestionCatalog()
        self.addCustList()

    def test_1(self):
        pass

