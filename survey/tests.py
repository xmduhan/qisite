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
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from services import PaperAdd_ErrorMessage, PaperAdd_ErrorCode
from account.models import User
import json
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import make_password, check_password
from account.tests import loginForTest, phoneForTest, passwordForTest


class SurveyModelTest(TestCase):
    '''
        数据模型的基本操作测试
    '''

    def addUser(self):
        user = account.models.User(name='tsUser', phone='1234567890', email='sample@example.com')
        user.save()
        self.tsUser = user

    def addPaper(self):
        paper = Paper(
            title='tsPaper', description='tsPaper.description', inOrder=True, lookBack=False, paging=False,
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
            type='Single', ord=1, contentLengh=0, valueMin=0, valueMax=0, confused=False, branchNumStyle='S1',
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

    def addFillblankQuestion(self):
        '''
            增加一个填空题
        '''
        fillblankQuestion = Question(
            type='Fillblank', ord=2, contentLengh=100, valueMin=0, valueMax=0, confused=False, branchNumStyle='S1',
            nextQuestion=None, paper=self.tsPaper, createBy=self.tsUser, modifyBy=self.tsUser
        )
        fillblankQuestion.save()
        self.tsFillblankQuestion = fillblankQuestion
        # 增加单选题的题干
        fillblankStem = Stem(text='填空题', question=fillblankQuestion, createBy=self.tsUser, modifyBy=self.tsUser)
        fillblankStem.save()
        self.tsFillblankStem = fillblankStem

    def addQuestions(self):
        self.addSingleQuestion()
        self.addFillblankQuestion()

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
        targetCust.defineInfo_set.add(targetCustInfo1)
        targetCust.save()
        # 2
        targetCustInfo2 = DefineInfo(
            name='附件信息2', value='附件信息2-内容', ord=1, createBy=self.tsUser, modifyBy=self.tsUser
        )
        targetCustInfo2.save()
        targetCust.defineInfo_set.add(targetCustInfo2)
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
        self.tsPaperCatalog = paperCatalog
        paperCatalogPaper = PaperCatalogPaper(
            paperCatalog=paperCatalog, paper=self.tsPaper, ord=0, createBy=self.tsUser, modifyBy=self.tsUser
        )
        paperCatalogPaper.save()
        self.tsPaperCatalogPaper = paperCatalogPaper


    def addQuestionCatalog(self):
        questionCatalog = QuestionCatalog(
            name='测试问题目录', code='TestQestionCatalog', parent=None, ord=0, createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        questionCatalog.save()
        self.tsQuestionCatalog = questionCatalog
        # 连接问题目录和问题
        # 1
        questionCatalogQuestion1 = QuestionCatalogQuestion(
            questionCatalog=questionCatalog, question=self.tsSingleQuestion, ord=2, createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        questionCatalogQuestion1.save()
        self.tsQuestionCatalogQuestion1 = questionCatalogQuestion1
        # 2
        questionCatalogQuestion2 = QuestionCatalogQuestion(
            questionCatalog=questionCatalog, question=self.tsFillblankQuestion, ord=1, createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        questionCatalogQuestion2.save()
        self.tsQuestionCatalogQuestion2 = questionCatalogQuestion2

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
        custListItem1.defineInfo_set.add(custListItemInfo1)
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
        custListItem2.defineInfo_set.add(custListItemInfo2)
        custListItem2.save()

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

    def test_get_catalog_paper(self):
        '''
            根据目录获取
        '''
        paperCatalog = self.tsPaperCatalog
        paperCount = paperCatalog.paper_set.count()
        self.assertEqual(paperCount, 1)
        paper = paperCatalog.paper_set.all()[0]
        self.assertEqual(paper.id, self.tsPaper.id)

    def test_get_user_survey_created(self):
        '''
            根据用户查找其名下调查
        '''
        user = self.tsUser
        surveyCount = user.surveyCreated_set.count()
        self.assertEqual(surveyCount, 1)
        survey = user.surveyCreated_set.all()[0]
        self.assertEqual(survey.id, self.tsSurvey.id)

    def test_get_user_paper_created(self):
        '''
            根据用户查找其名下的问卷定义
        '''
        user = self.tsUser
        paperCount = user.paperCreated_set.count()
        self.assertEqual(paperCount, 1)
        paper = user.paperCreated_set.all()[0]
        self.assertEqual(paper.id, self.tsPaper.id)

    def test_get_paper_question(self):
        '''
            根据问卷查找其问题定义
        '''
        paper = self.tsPaper
        questionCount = paper.question_set.count()
        self.assertEqual(questionCount, 2)
        question = paper.question_set.filter(type='Single')[0]
        self.assertEqual(question.id, self.tsSingleQuestion.id)

    def test_get_question_branch(self):
        '''
            根据问题查找其对应的选项定义
        '''
        question = self.tsSingleQuestion
        branchCount = question.branch_set.count()
        self.assertEqual(branchCount, 4)
        branches = question.branch_set.all()
        branchIds = [i.id for i in branches]
        #branchIds = branchIds[:3]
        self.assertIn(self.tsSingleBranch1.id, branchIds)
        self.assertIn(self.tsSingleBranch2.id, branchIds)
        self.assertIn(self.tsSingleBranch3.id, branchIds)
        self.assertIn(self.tsSingleBranch4.id, branchIds)

    def test_default_value_vaild(self):
        '''
            测试模型的默认值是否有效
        '''
        survey = self.tsSurvey
        self.assertEqual(survey.ipLimit, Survey._meta.get_field('ipLimit').default)
        self.assertEqual(survey.macLimit, Survey._meta.get_field('macLimit').default)

    def test_get_question_branches_in_order(self):
        '''
            测试对问题的选项进行排序
        '''
        question = self.tsSingleQuestion
        branches = question.branch_set.order_by('-ord')
        self.assertEqual(branches[0].id, self.tsSingleBranch4.id)

    def test_get_catalog_question_in_order(self):
        '''
            测试问题目录获取问题并排序
            这里主要我们在添加问题和目录的关联的时候，故意的将问题目录和问题间的关联的排序号(ord)，设置成和问题本身相反
        '''
        questionCatalog = self.tsQuestionCatalog
        question = questionCatalog.question_set.order_by('questioncatalogquestion__ord', 'ord')[0]
        self.assertEqual(question.id, self.tsFillblankQuestion.id)
        question = questionCatalog.question_set.order_by('ord')[0]
        self.assertEqual(question.id, self.tsSingleQuestion.id)


class PaperAddTest(TestCase):
    '''
        对问卷修改服务的测试
    '''

    def test_add_paper_no_login(self):
        setup_test_environment()
        client = Client()
        response = client.post(
            reverse('survey:service.paper.add'), {'title': 'test'}
        )
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], PaperAdd_ErrorCode.error)
        self.assertEquals(result['errorMessage'], PaperAdd_ErrorMessage.no_login)


    def test_add_paper_no_title(self):
        setup_test_environment()
        client = Client()
        # 创建用户并且用其登陆
        User(phone=phoneForTest, password=make_password(passwordForTest)).save()
        loginForTest(client, phoneForTest, passwordForTest)
        # 调用问卷添加服务
        response = client.post(reverse('survey:service.paper.add'), {})
        result = json.loads(response.content)
        self.assertEquals(result['errorCode'], PaperAdd_ErrorCode.error)
        self.assertContains(response, u'title:')
        self.assertContains(response, u'null')


