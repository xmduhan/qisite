# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import division
from django.test import TestCase
from models import *
import account.models
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from dateutil import parser
from account.models import User
import json, random, string
from django.contrib.auth.hashers import make_password, check_password
from account.tests import loginForTest, phoneForTest, passwordForTest
from django.core.signing import Signer
from django.db import transaction
from qisite.utils import updateModelInstance
from qisite.definitions import RESULT_CODE, RESULT_MESSAGE
from qisite.settings import domain
from BeautifulSoup import BeautifulSoup
from io import BytesIO
import copy


class TransactionTest(TestCase):
    def test_autocommit(self):
        step = 0
        title = "".join(random.sample(string.letters, 20))
        try:
            Paper(title=title).save()
            step = 1
            raise Exception()
        except:
            pass
        paperList = Paper.objects.filter(title=title)
        self.assertEqual(step, 1)  #  确认执行到了raise
        self.assertEqual(len(paperList), 1)  #  确认数据已经提交了

    def test_transaction_atomic(self):
        step = 0
        title = "".join(random.sample(string.letters, 20))
        try:
            with transaction.atomic():
                Paper(title=title).save()
                step = 1
                raise Exception()
        except Exception as e:
            print e
            pass
        paperList = Paper.objects.filter(title=title)
        self.assertEqual(step, 1)  # 确认执行到了raise
        self.assertEqual(len(paperList), 0)  # 确认数据已经被回滚了


class SurveyModelTest(TestCase):
    '''
        数据模型的基本操作测试
    '''
    fixtures = ['initial_data.json']

    def addUser(self):
        user = account.models.User(name='tsUser', phone='1234567890', email='sample@example.com')
        user.save()
        self.tsUser = user

    def addPaper(self):
        paper = Paper(
            title='tsPaper', description='tsPaper.description', inOrder=True, lookBack=False,
            createBy=self.tsUser, modifyBy=self.tsUser
        )
        paper.save()
        self.tsPaper = paper

    def addSurvey(self):
        survey = Survey(
            paper=self.tsPaper,  # 在没有问卷的情况下，是无法创建调查的
            targetOnly=True, state='?', shared=False, viewResult=False, resubmit=False, password='',
            hardCost=0, bonus=0, fee=0, validSampleLimit=0, createBy=self.tsUser, modifyBy=self.tsUser
            #survey.ipLimit = 5  #survey.ipLimit = 5  # 用来测试默认值
        )
        survey.save()
        self.tsSurvey = survey

    def addSingleQuestion(self):
        # 增加一个单选题
        singleQuestion = Question(
            type='Single', text='问题1', ord=1, contentLength=0, valueMin=0, valueMax=0, confused=False,
            branchNumStyle='S1',
            nextQuestion=None, paper=self.tsPaper, createBy=self.tsUser, modifyBy=self.tsUser
        )
        singleQuestion.save()
        self.tsSingleQuestion = singleQuestion

        # 增加题干的资源
        singleResource = Resource(
            resourceType='Picture', resourceUrl='http://example.com/picture/111', width=640, height=480,
            question=singleQuestion, createBy=self.tsUser, modifyBy=self.tsUser
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
            type='Fillblank', ord=2, contentLength=100, valueMin=0, valueMax=0, confused=False, branchNumStyle='S1',
            nextQuestion=None, paper=self.tsPaper, createBy=self.tsUser, modifyBy=self.tsUser
        )
        fillblankQuestion.save()
        self.tsFillblankQuestion = fillblankQuestion
        # 增加单选题的题干
        #fillblankStem = Stem(text='填空题', question=fillblankQuestion, createBy=self.tsUser, modifyBy=self.tsUser)
        #fillblankStem.save()
        #self.tsFillblankStem = fillblankStem

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
            targetCust=self.tsTargetCust, user=None, ipAddress='127.0.0.1',
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


    def test_branch_getSystemPredefined(self):
        '''
        测试通过选项获取系统预定义出口（特殊问题）
        如果出现问题一般是数据缺失
        '''
        branch = Branch()
        questionList = branch.getSystemPredefined()
        self.assertEquals(len(questionList), 2)


class SurveyDeleteTest(TestCase):
    '''
        问卷删除服务的测试用例
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.client = Client()
        self.user = User.objects.get(code='duhan')
        self.paper = self.user.paperCreated_set.get(code='paper-instance-test01')  #网购客户满意度调查(非定向)
        self.survey = Survey.objects.get(paper=self.paper)
        self.user_other = User.objects.get(code='zhangjianhua')
        self.paper_other = self.user_other.paperCreated_set.get(code='paper-instance-test02')  #净推介值调查
        self.survey_other = Survey.objects.get(paper=self.paper_other)
        loginForTest(self.client, self.user.phone, '123456')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': self.survey.getIdSigned()}
        self.data_bad_signature = {'id': self.survey.id}
        self.data_no_privilege = {'id': self.survey_other.getIdSigned()}
        #
        self.serviceUrl = reverse('survey:service.survey.delete')


    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_not_exist(self):
        '''
            测试对象不存在的情况
        '''
        self.survey.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_no_privilege(self):
        '''
            测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            成功删除
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经不能存在了
        surveyList = Survey.objects.filter(id=self.survey.id)
        # 删除文件不是直接删除，仅标识状态
        self.assertEqual(len(surveyList), 1)
        # 确认状态为删除状态
        survey = surveyList[0]
        self.assertEqual(survey.state, 'P')


class PaperAddTest(TestCase):
    '''
        对问卷修改服务(paperAdd)的测试
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        User(phone=phoneForTest, password=make_password(passwordForTest)).save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 设定service url
        self.serviceUrl = reverse('survey:service.paper.add')

    def test_add_paper_no_login(self):
        '''
            测试没有登录就调用服务的情况
        '''
        # 创建一个新的Client，而不是使用self.client，因为self.client已经在setUP中登录了。
        client = Client()
        response = client.post(self.serviceUrl, {'title': 'test'})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)  # 没有登录错误


    def test_add_paper_no_title(self):
        '''
            测试没有提供标题的情况
        '''
        client = self.client
        # 调用问卷添加服务
        response = client.post(self.serviceUrl, {'test': '123'})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)  # 数据校验错
        self.assertIn('title', result['validationMessage'])  # 校验错误信息中含title

    def test_add_paper_success(self):
        '''
            测试成功添加的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {'title': 'test'})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


class PaperModifyTest(TestCase):
    '''
        问卷修改服务(paperModify)测试
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper_123', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.paper.modify')

        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': signer.sign(self.paper.id), 'inOrder': not self.paper.inOrder}
        self.data_bad_signature = {'id': self.paper.id, 'inOrder': not self.paper.inOrder}
        self.data_no_privilege = {'id': signer.sign(self.paper_other.id), 'inOrder': not self.paper_other.inOrder}
        self.data_validation_error = {'id': signer.sign(self.paper.id), 'questionNumStyle': '未知'}
        self.data_tamper = {'id': signer.sign(self.paper.id), 'createBy': self.user_other.id}

    def test_no_login(self):
        '''
            测试没有登陆的情况
        '''
        # 使用新创建的client(未登录)，而不是self.client（已登录)
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_paper_not_exist(self):
        '''
            测试修改不存在问卷的情况
        '''
        # 删除保证数据不存在
        self.paper.delete()
        #
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_privilege(self):
        '''
            尝试修改不是自己的问卷
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_validation_error(self):
        '''
            尝试修改不是自己的问卷
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_validation_error)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)

    def test_success(self):
        '''
           测试成功修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid, format='json')
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经被修改
        paper = Paper.objects.filter(id=self.paper.id)[0]
        self.assertNotEquals(paper.inOrder, self.paper.inOrder)

    def test_tamper(self):
        '''
           确认数据不会摆篡改
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_tamper)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据不会被篡改
        paper = Paper.objects.filter(id=self.paper.id)[0]
        self.assertEquals(paper.createBy, self.paper.createBy)


class PaperDeleteTest(TestCase):
    '''
        问卷删除服务的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper_123', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.paper.delete')

        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': signer.sign(self.paper.id)}
        self.data_bad_signature = {'id': self.paper.id, }
        self.data_no_privilege = {'id': signer.sign(self.paper_other.id)}

    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_not_exist(self):
        '''
            测试对象不存在的情况
        '''
        self.paper.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_no_privilege(self):
        '''
            测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            成功删除
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经不能存在了
        paperList = Paper.objects.filter(id=self.paper.id)
        self.assertEquals(len(paperList), 0)


class QuestionAddTest(TestCase):
    '''
        问题添加服务(questionAdd)测试
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper_123', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.question.add')
        # 准备提交的测试数据
        signer = Signer()
        questionText = 'text123'
        questionType = 'Single'
        self.data_valid = {'paper': signer.sign(self.paper.id), 'text': questionText, 'type': questionType}
        self.data_bad_signature = {'paper': self.paper.id, 'text': questionText, 'type': questionType}
        self.data_no_privilege = {'paper': signer.sign(self.paper_other.id), 'text': questionText, 'type': questionType}
        self.data_invalid_type = {'paper': signer.sign(self.paper.id), 'text': questionText, 'type': 'EndValid'}
        self.data_invalid_length = {
            'paper': signer.sign(self.paper.id), 'text': questionText, 'type': questionType, 'contentLength': 100}


    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_paper(self):
        '''
            测试没有提供问卷的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试篡改数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_paper_no_exist(self):
        '''
            测试问卷不存在的情况
        '''
        self.paper.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_privilege(self):
        '''
            测试在非本用户添加的问卷中添加
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_invalid_type(self):
        '''
            测试使用无效的问题类型
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_invalid_type)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)

    def test_invalid_length(self):
        '''
            测试为选择设置问题的长度
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_invalid_length)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)

    def test_sucess(self):
        '''
            测试成功添加的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


class QuestionModifyTest(TestCase):
    '''
        问题修改的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        self.question = Question(
            type='Single', text='question', ord=1, createBy=self.user, modifyBy=self.user, paper=self.paper)
        self.question.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        self.question_other = Question(
            type='Single', text='question_other', ord=1, createBy=self.user_other, modifyBy=self.user_other,
            paper=self.paper_other)
        self.question_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.question.modify')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': signer.sign(self.question.id), 'confused': not self.question.confused}
        self.data_bad_signature = {'id': self.question.id, 'confused': not self.question.confused}
        self.data_no_privilege = \
            {'id': signer.sign(self.question_other.id), 'confused': not self.question_other.confused}
        self.data_validation_error = {'id': signer.sign(self.question.id), 'branchNumStyle': '未知'}
        self.data_tamper = {'id': signer.sign(self.question.id), 'createBy': self.user_other.id}

    def test_no_login(self):
        '''
            测试没有登陆的情况
        '''
        # 使用新创建的client(未登录)，而不是self.client（已登录)
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数据签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_question_not_exist(self):
        '''
            测试修改不存在的问题
        '''
        self.question.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_privilege(self):
        '''
            测试修改非自己创建的问题
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_validation_error(self):
        '''
            测试改入一些非法的数据
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_validation_error)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)

    def test_success(self):
        '''
            测试修改成功的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经被修改
        question = Question.objects.filter(id=self.question.id)[0]
        self.assertNotEquals(question.confused, self.question.confused)

    def test_tamper(self):
        client = self.client
        response = client.post(self.serviceUrl, self.data_tamper)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确定数据不会被篡改
        question = Question.objects.filter(id=self.question.id)[0]
        self.assertEquals(question.createBy, self.question.createBy)


class QuestionDeleteTest(TestCase):
    '''
        问题删除服务的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        self.question = Question(
            type='Single', text='question', ord=1, createBy=self.user, modifyBy=self.user, paper=self.paper)
        self.question.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        self.question_other = Question(
            type='Single', text='question_other', ord=1, createBy=self.user_other, modifyBy=self.user_other,
            paper=self.paper_other)
        self.question_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.question.delete')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': signer.sign(self.question.id)}
        self.data_bad_signature = {'id': self.question.id}
        self.data_no_privilege = {'id': signer.sign(self.question_other.id)}

    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_not_exist(self):
        '''
            测试对象不存在的情况
        '''
        self.question.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_no_privilege(self):
        '''
            测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            成功删除
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经不能存在了
        questionList = Question.objects.filter(id=self.question.id)
        self.assertEquals(len(questionList), 0)


class BranchAddTest(TestCase):
    '''
        题支新增测试
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        self.question = Question(
            type='Single', text='question', ord=1, createBy=self.user, modifyBy=self.user, paper=self.paper)
        self.question.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        self.question_other = Question(
            type='Single', text='question_other', ord=1, createBy=self.user_other, modifyBy=self.user_other,
            paper=self.paper_other)
        self.question_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.branch.add')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'question': signer.sign(self.question.id), 'text': 'branch1'}
        self.data_bad_signature = {'question': self.question.id, 'text': 'branch1'}
        self.data_no_privilege = {'question': signer.sign(self.question_other.id), 'text': 'branch1'}

    def test_no_login(self):
        '''
            测试没有登陆的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)


    def test_no_question(self):
        '''
            测试没有提供问题的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数据签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_question_no_exist(self):
        '''
            测试提供的问题已经不存在的情况
        '''
        self.question.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_privilege(self):
        '''
            测试没有权限的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            测试成功的操作
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


class BranchModifyTest(TestCase):
    '''
        题支修改服务的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        self.question = Question(
            type='Single', text='question', ord=1, createBy=self.user, modifyBy=self.user, paper=self.paper)
        self.question.save()
        self.branch = Branch(text='branch', question=self.question, ord=1, createBy=self.user, modifyBy=self.user)
        self.branch.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        self.question_other = Question(
            type='Single', text='question_other', ord=1, createBy=self.user_other, modifyBy=self.user_other,
            paper=self.paper_other)
        self.question_other.save()
        self.branch_other = Branch(
            text='branch', question=self.question_other, ord=1, createBy=self.user_other, modifyBy=self.user_other)
        self.branch_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.branch.modify')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': signer.sign(self.branch.id), 'text': 'branch1'}
        self.data_bad_signature = {'id': self.branch.id, 'text': 'branch1'}
        self.data_no_privilege = {'id': signer.sign(self.branch_other.id), 'text': 'branch1'}
        self.data_valid_null_next = {'id': signer.sign(self.branch.id), 'nextQuestion': 'null'}

    def test_no_login(self):
        '''
            测试没有登陆的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_branch_not_exist(self):
        '''
            测试选项不存在的情况
        '''
        self.branch.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_privilege(self):
        '''
            测试选项不存在的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success_null_next(self):
        '''
            测试操作成功的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid_null_next)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)

    def test_success(self):
        '''
            测试操作成功的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


class BranchDeleteTest(TestCase):
    '''
        选项删除服务的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        self.question = Question(
            type='Single', text='question', ord=1, createBy=self.user, modifyBy=self.user, paper=self.paper)
        self.question.save()
        self.branch = Branch(text='branch', question=self.question, ord=1, createBy=self.user, modifyBy=self.user)
        self.branch.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        self.question_other = Question(
            type='Single', text='question_other', ord=1, createBy=self.user_other, modifyBy=self.user_other,
            paper=self.paper_other)
        self.question_other.save()
        self.branch_other = Branch(
            text='branch', question=self.question_other, ord=1, createBy=self.user_other, modifyBy=self.user_other)
        self.branch_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.branch.delete')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': signer.sign(self.branch.id)}
        self.data_bad_signature = {'id': self.branch.id}
        self.data_no_privilege = {'id': signer.sign(self.branch_other.id)}

    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_not_exist(self):
        '''
            测试对象不存在的情况
        '''
        self.branch.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_no_privilege(self):
        '''
            测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            成功删除
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经不能存在了
        branchList = Branch.objects.filter(id=self.branch.id)
        self.assertEquals(len(branchList), 0)


class AddDefaultSingleQuestionTest(TestCase):
    '''
        新增默认单选题服务的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper_123', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.question.addDefaultSingleQuestion')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'paper': signer.sign(self.paper.id)}
        self.data_bad_signature = {'paper': self.paper.id}
        self.data_no_privilege = {'paper': signer.sign(self.paper_other.id)}
        self.data_invalid_type = {'paper': signer.sign(self.paper.id)}

    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供paper的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试篡改数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)


    def test_no_privilege(self):
        '''
            测试没有权限的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            测试成功的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


class AddDefaultBranchTest(TestCase):
    '''
        新增默认选项服务的测试用例
    '''

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.user = User(phone=phoneForTest, password=make_password(passwordForTest))
        self.user.save()
        self.client = Client()
        loginForTest(self.client, phoneForTest, passwordForTest)
        # 创建一个用于测试的Paper
        self.paper = Paper(title='paper', createBy=self.user, modifyBy=self.user)
        self.paper.save()
        self.question = Question(
            type='Single', text='question', ord=1, createBy=self.user, modifyBy=self.user, paper=self.paper)
        self.question.save()
        # 创建另一个测试用户
        self.user_other = User(phone='123')
        self.user_other.save()
        self.paper_other = Paper(title='paper_other', createBy=self.user_other, modifyBy=self.user_other)
        self.paper_other.save()
        self.question_other = Question(
            type='Single', text='question_other', ord=1, createBy=self.user_other, modifyBy=self.user_other,
            paper=self.paper_other)
        self.question_other.save()
        # 设定service url
        self.serviceUrl = reverse('survey:service.branch.addDefaultBranch')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'question': signer.sign(self.question.id)}
        self.data_bad_signature = {'question': self.question.id}
        self.data_no_privilege = {'question': signer.sign(self.question_other.id)}

    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_question(self):
        '''
            测试没有提供问题的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_no_privilege(self):
        '''
            测试没有权限的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_bad_signature(self):
        '''
            没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_success(self):
        '''
            测试添加成功的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


    def test_session(self):
        '''

        '''
        client = self.client
        client.session


class PaperCreateInstanceTest(TestCase):
    '''
    通过问卷模板创建一个新的问卷的测试用例
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        self.user = User.objects.get(code='duhan')
        self.paper = Paper.objects.get(code='paper-template-01', type='T')  #网购客户满意度调查(非定向)

    def test_createPaperInstance(self):
        newPaper = self.paper.createPaperInstance(self.user)
        # 检查对象是否是新创建的
        self.assertNotEqual(newPaper, self.paper)
        # 检查文件类型是否是实例
        self.assertNotEqual(self.paper.type, newPaper.type)
        self.assertEqual(newPaper.type, 'I')
        # 检查对象内容是否和原来一样
        self.assertEqual(newPaper.title, self.paper.title)

        # 获取原问卷的问题和选项列表
        oldQuestionList = list(self.paper.question_set.all())
        self.assertEqual(len(oldQuestionList), 4)
        oldBranchList = []
        for question in oldQuestionList:
            oldBranchList.extend(list(question.branch_set.all()))
        self.assertEqual(len(oldBranchList), 11)

        # 获取新的问卷的问题和选项列表
        newQuestionList = list(newPaper.question_set.all())
        self.assertEqual(len(newQuestionList), len(oldQuestionList))
        newBranchList = []
        for question in newQuestionList:
            newBranchList.extend(list(question.branch_set.all()))
        self.assertEqual(len(newBranchList), len(oldBranchList))

        # 计算新问题列表和旧问题列表间的交集
        intersection = set(oldQuestionList).intersection(set(newQuestionList))
        self.assertEqual(len(intersection), 0)

        # 计算新选项列表和旧选项列表间的交集
        intersection = set(oldBranchList).intersection(set(newBranchList))
        self.assertEqual(len(intersection), 0)

        # 确定新问题的创建时间都比旧的要大
        for newQuestion in newQuestionList:
            for oldQuestion in oldQuestionList:
                self.assertGreater(question.createTime, oldQuestion.createTime)

        # 确定新选项的创建时间都比旧的要大
        for newBranch in newBranchList:
            for oldBranch in oldBranchList:
                self.assertGreater(newBranch.createTime, oldBranch.createTime)

        # 检查问卷跳转结构
        question1 = newPaper.question_set.get(ord=0)
        branch1_1 = question1.branch_set.get(ord=0)
        branch1_2 = question1.branch_set.get(ord=1)
        question2 = newPaper.question_set.get(ord=1)
        branch2_1 = question2.branch_set.get(ord=0)
        branch2_2 = question2.branch_set.get(ord=1)
        branch2_3 = question2.branch_set.get(ord=2)
        question3 = newPaper.question_set.get(ord=2)
        question4 = newPaper.question_set.get(ord=3)
        self.assertEqual(branch1_1.nextQuestion, None)
        self.assertEqual(branch1_2.nextQuestion.type, 'EndInvalid')
        self.assertEqual(branch2_1.nextQuestion.type, 'EndValid')
        self.assertEqual(branch2_2.nextQuestion, question3)
        self.assertEqual(branch2_3.nextQuestion, question4)


class UpdateModelInstanceTest(TestCase):
    '''
    updateModelInstance(通过字段更新数据模型实例的过程)的测试用例
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        admin = User.objects.get(code='admin')
        user = User.objects.get(code='duhan')
        paper = Paper.objects.get(code='paper-template-01', type='T')  #网购客户满意度调查(非定向)
        survey = Survey()
        survey.createBy = admin
        survey.modifyBy = admin
        survey.save()
        self.survey = survey
        self.admin = admin
        self.user = user
        self.paper = paper

    def reloadSurvey(self):
        self.survey = Survey.objects.get(id=self.survey.id)
        return self.survey

    def test_update_string(self):
        '''
        尝试对字符串字段进行修改
        '''
        survey = self.reloadSurvey()
        survey.state = '1'
        updateModelInstance(survey, {'state': '2'})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.state, '2')
        # 如果传入是一个数字
        updateModelInstance(survey, {'state': 3})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.state, '3')

    def test_update_number(self):
        '''
        尝试更新一个整型的字段
        '''
        survey = self.reloadSurvey()
        survey.bonus = 1
        # 测试正常修改值是否生效
        updateModelInstance(survey, {'bonus': 2})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.bonus, 2)
        # 如果传入是一个字符串
        updateModelInstance(survey, {'bonus': '3'})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.bonus, 3)

    def test_update_bool(self):
        '''
        测试更新一个bool变量
        '''
        survey = self.reloadSurvey()
        # 测试正常修改值是否生效
        survey.shared = False
        updateModelInstance(survey, {'shared': True})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.shared, True)
        # 测试传入'false'(来自json)字符串情况
        survey.shared = False
        updateModelInstance(survey, {'shared': 'true'})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.shared, True)
        # 测试传入'on'字符串情况
        survey.shared = False
        updateModelInstance(survey, {'shared': 'on'})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.shared, True)
        # 测试传入'是'字符串情况
        survey.shared = False
        updateModelInstance(survey, {'shared': '是'})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.shared, True)

    def test_tamper_createBy(self):
        '''
        测试数据篡改保护
        '''
        survey = self.reloadSurvey()
        self.assertEqual(survey.createBy, self.admin)
        # 测试默认参数情况数据是无法篡改的
        updateModelInstance(survey, {'createBy': self.user})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.createBy, self.admin)
        # 特殊要求不要进行过滤,就可以修改
        updateModelInstance(survey, {'createBy': self.user}, excludeFields=[])
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.createBy, self.user)

    def test_foreignKey_load(self):
        '''
        测试外键的加载
        '''
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, None)
        # 放入一个id
        updateModelInstance(survey, {'paper': self.paper.id})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, self.paper)
        # 测试修改成一个空字符串
        updateModelInstance(survey, {'paper': ''})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, None)
        # 测试放入一个字符串id
        updateModelInstance(survey, {'paper': str(self.paper.id)})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, self.paper)
        # 测试使用'null'(可能来自json)
        updateModelInstance(survey, {'paper': 'null'})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, None)

    def test_load_signed_id(self):
        '''
        测试加载经过数字签名的外键id
        '''
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, None)
        # 加载一个经过数字签名的id
        signer = Signer()
        paperIdSigned = signer.sign(self.paper.id)
        updateModelInstance(survey, {'paper': paperIdSigned}, tryUnsigned=True)
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.paper, self.paper)

    def test_update_time(self):
        '''
        测试日期格式字段的处理
        '''
        # 使用字符串进行修改
        survey = self.reloadSurvey()
        dateString1 = '2014-01-01'
        date1 = parser.parse(dateString1)
        updateModelInstance(survey, {'publishTime': dateString1})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.publishTime, date1)

        # 使用日期变量进行修改
        dateString2 = '2014-02-01'
        date2 = parser.parse(dateString2)
        updateModelInstance(survey, {'publishTime': date2})
        survey.save()
        survey = self.reloadSurvey()
        self.assertEqual(survey.publishTime, date2)


class CustListAddTest(TestCase):
    '''
        对问卷修改服务(custListAdd)的测试
    '''
    fixtures = ['initial_data.json']


    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        user = User.objects.get(code='duhan')
        self.client = Client()
        loginForTest(self.client, user.phone, '123456')
        # 设定service url
        self.serviceUrl = reverse('survey:service.custList.add')

        # 准备要提交的数据
        self.data_valid = {'name': 'test'}
        self.date_no_title = {'test': '123'}
        #self.data_tamper = {'id': 'createBy':}

    def test_add_custList_no_login(self):
        '''
            测试没有登录就调用服务的情况
        '''
        # 创建一个新的Client，而不是使用self.client，因为self.client已经在setUP中登录了。
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)  # 没有登录错误


    def test_add_custList_no_title(self):
        '''
            测试没有提供清单名称的情况
        '''
        client = self.client
        # 调用问卷添加服务
        response = client.post(self.serviceUrl, self.date_no_title)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)  # 数据校验错
        self.assertIn('name', result['validationMessage'])  # 校验错误信息中含title

    def test_add_custList_success(self):
        '''
            测试成功添加的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)


class CustListDeleteTest(TestCase):
    '''
        问卷删除服务的测试用例
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.client = Client()
        self.user = User.objects.get(code='duhan')
        self.custList = self.user.custListCreated_set.get(name=u'2013年发展的客户')
        self.user_other = User.objects.get(code='zhangjianhua')
        self.custList_other = self.user_other.custListCreated_set.get(name=u'EMBA同学名单')
        # 登录
        loginForTest(self.client, self.user.phone, '123456')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': self.custList.getIdSigned()}
        self.data_bad_signature = {'id': self.custList.id}
        self.data_no_privilege = {'id': self.custList_other.getIdSigned()}
        #
        self.serviceUrl = reverse('survey:service.custList.delete')


    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_not_exist(self):
        '''
            测试对象不存在的情况
        '''
        self.custList.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_no_privilege(self):
        '''
            测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            成功删除
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经不能存在了
        custListList = CustList.objects.filter(id=self.custList.id)
        self.assertEqual(len(custListList), 0)


class CustListItemAddTest(TestCase):
    '''
        对问卷修改服务(custListAdd)的测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        # 读取测试用户和清单
        user = User.objects.get(code='duhan')
        custList = user.custListCreated_set.get(name=u'2013年发展的客户')
        user_other = User.objects.get(code='zhangjianhua')
        custList_other = user_other.custListCreated_set.get(name=u'EMBA同学名单')

        # 创建客户端
        self.client = Client()
        loginForTest(self.client, user.phone, '123456')
        # 设定service url
        self.serviceUrl = reverse('survey:service.custListItem.add')

        # 准备要提交的数据
        self.data_valid = {'custList': custList.getIdSigned(), 'name': 'test01', 'phone': user.phone}
        self.data_no_id = {'name': 'test01', 'phone': user.phone}
        self.data_no_name = {'custList': custList.getIdSigned()}
        self.data_no_phone = {'custList': custList.getIdSigned(), 'name': 'test01'}
        self.data_bad_signature = {'custList': custList.id, 'name': 'test01'}
        self.data_no_privilege = {'custList': custList_other.getIdSigned(), 'name': 'test01', 'phone': user.phone}
        self.data_bad_phone = {'custList': custList.getIdSigned(), 'name': 'test01', 'phone': '123456'}
        self.data_bad_email = {'custList': custList.getIdSigned(), 'name': 'test01', 'email': '123456'}

    def test_add_custListItem_no_login(self):
        '''
            测试没有登录就调用服务的情况
        '''
        # 创建一个新的Client，而不是使用self.client，因为self.client已经在setUP中登录了。
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)  # 没有登录错误

    def test_add_custListItem_no_id(self):
        '''
        测试没有提供custListId的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_id)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)  # 没有提供id


    def test_add_custListItem_bad_signature(self):
        '''
        测试非法的数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)


    def test_add_custListItem_no_name(self):
        '''
            测试没有提供清单名称的情况
        '''
        client = self.client
        # 调用问卷添加服务
        response = client.post(self.serviceUrl, self.data_no_name)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)  # 数据校验错
        self.assertIn('name', result['validationMessage'])  # 校验错误信息中含name


    def test_add_custListItem_no_phone(self):
        '''
        测试没有提供phone的情况
        '''
        client = self.client
        # 调用问卷添加服务
        response = client.post(self.serviceUrl, self.data_no_phone)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)  # 数据校验错
        self.assertIn('phone', result['validationMessage'])  # 校验错误信息中含name

    def test_add_custListItem_bad_phone(self):
        '''
        测试提供的是非法的手机号码情况
        '''
        client = self.client
        # 调用问卷添加服务
        response = client.post(self.serviceUrl, self.data_bad_phone)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.VALIDATION_ERROR)  # 数据校验错
        self.assertIn('phone', result['validationMessage'])  # 校验错误信息中含name

    def test_add_custListItem_no_privilege(self):
        '''
        测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)  # 出错
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)  # 没有权限

    def test_add_custListItem_success(self):
        '''
            测试成功添加的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        custListItemId = result['custListItemId']
        custListItemList = CustListItem.objects.filter(id=custListItemId)
        self.assertEqual(len(custListItemList), 1)


class CustListItemDeleteTest(TestCase):
    '''
        问卷删除服务的测试用例
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        # 创建用户并且用其登陆
        self.client = Client()
        self.user = User.objects.get(code='duhan')
        self.custList = self.user.custListCreated_set.get(name=u'2013年发展的客户')
        self.custListItem = self.custList.custListItem_set.all()[0]
        self.user_other = User.objects.get(code='zhangjianhua')
        self.custList_other = self.user_other.custListCreated_set.get(name=u'EMBA同学名单')
        self.custListItem_other = self.custList_other.custListItem_set.all()[0]
        # 登录
        loginForTest(self.client, self.user.phone, '123456')
        # 准备提交的测试数据
        signer = Signer()
        self.data_valid = {'id': self.custListItem.getIdSigned()}
        self.data_bad_signature = {'id': self.custListItem.id}
        self.data_no_privilege = {'id': self.custListItem_other.getIdSigned()}
        #
        self.serviceUrl = reverse('survey:service.custListItem.delete')

    def test_no_login(self):
        '''
            测试没有登录的情况
        '''
        client = Client()
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_LOGIN)

    def test_no_id(self):
        '''
            测试没有提供id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
            测试没有进行数字签名的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_not_exist(self):
        '''
            测试对象不存在的情况
        '''
        self.custList.delete()
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.OBJECT_NOT_EXIST)

    def test_no_no_privilege(self):
        '''
            测试没有权限修改的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_success(self):
        '''
            成功删除
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 确认数据已经不能存在了
        custListItemList = CustListItem.objects.filter(id=self.custListItem.id)
        self.assertEqual(len(custListItemList), 0)


class TargetLessSurveyAnswerTest(TestCase):
    '''
    无定向调查的提交规则测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        self.client = Client()
        self.survey = Survey.objects.get(code='survey-targetless-01')  #网购客户满意度调查(非定向)
        self.paper = self.survey.paper

        # 确认该调查为非定向调查
        self.assertIsNone(self.survey.custList)
        # 确定允许重复填写答案
        self.assertEqual(self.survey.resubmit, True)
        # 确定没有设置调查密码
        self.assertEqual(self.survey.password, '')
        # 确定是非匿名调查
        self.assertFalse(self.survey.anonymous)
        # 确认是允许查看结果的
        self.assertTrue(self.survey.viewResult)

        # 相关的url连接
        self.answerUrl = reverse('survey:view.survey.answer.render', args=[self.survey.id])
        self.answerSubmitUrl = reverse('survey:view.survey.answer.submit')

        # 相关的页面模板地址
        self.answerTemplate = 'survey/surveyAnswerAll.html'
        self.messageTemplate = 'www/message.html'
        self.answeredTemplate = 'survey/surveyAnswered.html'
        self.surveyLoginTemplate = 'survey/surveyLogin.html'

        # 生成一个合法的答卷数据，供后面的过程提交使用
        data_valid = {}
        questionIdList = []
        data_valid['surveyId'] = self.survey.getIdSigned()
        for question in self.paper.question_set.all():
            questionIdList.append(question.getIdSigned())
            data_valid[question.getIdSigned()] = question.branch_set.all()[0].getIdSigned()
        data_valid['questionIdList'] = questionIdList
        self.data_valid = copy.copy(data_valid)
        data_valid['resubmit'] = True
        self.data_valid_resubmit = copy.copy(data_valid)

    def test_enter_answer_page(self):
        '''
        检查非定向调查是否能够直接进入答题页面
        '''
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        # 检查是否直接转向答题模板
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)
        # 确认数据
        survey = response.context['survey']
        self.assertEqual(self.survey.id, survey.id)
        paper = response.context['paper']
        self.assertEqual(self.survey.paper.id, paper.id)


    def test_answer_submit_success(self):
        '''
        测试提交问卷信息
        '''
        client = self.client
        sampleCount = self.survey.paper.sample_set.count()

        # 提交到服务器
        response = client.post(self.answerSubmitUrl, self.data_valid)
        self.assertEqual(response.status_code, 200)

        # 检查提交的页面是否成功
        self.assertEqual(response.templates[0].name, self.messageTemplate)

        # 检查是否返回成功信息
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 确认样本数量增加了一个
        self.assertEqual(self.survey.paper.sample_set.count(), sampleCount + 1)

        # 确认question数量和sample相同
        ## 获取最新添加的一个sample
        sample = self.survey.paper.sample_set.order_by('-createTime')[0]
        self.assertEqual(sample.sampleitem_set.count(), self.survey.paper.question_set.count())


    def test_answer_resubmit_without_flag(self):
        '''
        确定测试重复提交会失败
        '''
        client = self.client

        # 第1次提交页面返回成功
        response = client.post(self.answerSubmitUrl, self.data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 第2次提交页面返回失败
        response = client.post(self.answerSubmitUrl, self.data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

        # 第2次不单是不能提交而且连答题页面都不能进去
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        # 检查是否转向重填提示
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

    def test_answer_resubmit_with_flag(self):
        '''
        测试使用重提交标志进行重新提交
        '''
        client = self.client

        # 记录样本数量已便后面做数量比较
        count0 = self.survey.paper.sample_set.count()

        # 第1次提交页面返回成功
        response = client.post(self.answerSubmitUrl, self.data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 填写完问卷以后样本数量加1
        count1 = self.survey.paper.sample_set.count()
        self.assertEqual(count0 + 1, count1)

        # 第2次仍然可以成功
        response = client.post(self.answerSubmitUrl, self.data_valid_resubmit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 重填样本数量不能增加
        count2 = self.survey.paper.sample_set.count()
        self.assertEqual(count1, count2)

        # 增加提交重填标志可以再次进入填题页面
        response = self.client.get(self.answerUrl, {'resubmit': True})
        self.assertEqual(response.status_code, 200)
        # 检查是否转向重填提示
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)

        # 测试是否提供上次填写的答案
        # 注意：这里已经假设了该问卷中全部都是单选题
        # 读取上次提交所有选项
        sample = self.survey.paper.sample_set.get(session=client.session.session_key)
        soup = BeautifulSoup(response.content)
        signer = Signer()
        for sampleItem in sample.sampleitem_set.all():
            for branch in sampleItem.branch_set.all():
                input = soup.find(attrs={
                    "name": signer.sign(sampleItem.question.id),
                    'value': signer.sign(branch.id)
                })
                self.assertEqual(input.get('checked'), 'checked')


    def test_answer_resubmit_with_flag_without_survey_flag(self):
        '''
        使用重复填写标志，但是问卷本身不支持重复填写
        '''
        client = self.client

        # 修改resubmit为False
        self.survey.resubmit = False
        self.survey.save()

        # 第1次提交页面返回成功
        response = client.post(self.answerSubmitUrl, self.data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 第2次提交是不能成功的
        response = client.post(self.answerSubmitUrl, self.data_valid_resubmit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

        # 答过之后页面都进不去
        response = self.client.get(self.answerUrl, {'resubmit': True})
        self.assertEqual(response.status_code, 200)
        # 检查是否转向重填提示
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)

        # 确认页面没有生成重填按钮
        #self.assertNotContains(response, u'重填')
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"id": "resubmitButton"})
        self.assertIsNone(input)


    def test_enter_page_with_password(self):
        '''
        测试有设置密码的情况下，进入页面需要提供密码。
        '''
        client = self.client
        # 为调查设置密码
        self.survey.password = '123456'
        self.survey.save()

        # 没有提供密码条状到登录页面
        response = self.client.get(self.answerUrl, {})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.surveyLoginTemplate)

        # 提供错误密码提示错误
        response = self.client.get(self.answerUrl, {'password': '111'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)


        # 提供密码可以正常进入页面
        response = self.client.get(self.answerUrl, {'password': self.survey.password})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)


        # 检查页面是否有包含密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))


    def test_submit_with_password(self):
        '''
        测试有设置密码的情况下，提交需要提供密码。
        '''
        client = self.client
        # 为调查设置密码
        self.survey.password = '123456'
        self.survey.save()

        # 进入调查页面
        response = self.client.get(self.answerUrl, {'password': self.survey.password})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')

        # 不提供密码，提交失败
        data_valid = copy.copy(self.data_valid)
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)

        # 提供密码就能提交成功
        data_valid = copy.copy(self.data_valid)
        data_valid['passwordEncoded'] = passwordEncoded
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 再次提交检查重填提交页面是否包含隐藏密码
        data_valid = copy.copy(self.data_valid)
        data_valid['passwordEncoded'] = passwordEncoded
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answeredTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))

        # 利用页面的隐藏密码重新交进入答题
        response = self.client.get(self.answerUrl, {'resubmit': True, 'passwordEncoded': passwordEncoded})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)

    def test_resubmit_with_password_without_survey_flag(self):
        '''
        调查设置了密码，但是调查是不允许重填的
        '''
        client = self.client
        # 为调查设置密码
        self.survey.password = '123456'
        #self.survey.resubmit = False
        self.survey.save()

        ############################## 第1次提交 #############################
        # 进入调查页面
        response = self.client.get(self.answerUrl, {'password': self.survey.password})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))

        # 提交成功
        data_valid = copy.copy(self.data_valid)
        data_valid['passwordEncoded'] = passwordEncoded
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        ############################## 第2次提交 #############################
        # 进入调查页面(返回的是已经答过页面)
        response = self.client.get(self.answerUrl, {'password': self.survey.password})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))

        # 附上重提交标识和隐藏密码再次进入页面
        response = self.client.get(self.answerUrl, {'passwordEncoded': passwordEncoded, 'resubmit': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.answerTemplate, response.templates[0].name),
        soup = BeautifulSoup(response.content)
        # 读取页面（答题页面）中的隐藏密码并检验
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))

        # 第2次提交返回失败
        data_valid = copy.copy(self.data_valid)
        data_valid['passwordEncoded'] = passwordEncoded
        data_valid['resubmit'] = True
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)


    def test_submit_expired_survey(self):
        '''
        测试提交过期的调查
        '''
        client = self.client

        # 修改调查使之过期
        self.survey.endTime = datetime.now()
        self.survey.save()

        # 过期后是无法提交的
        response = client.post(self.answerSubmitUrl, self.data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_EXPIRED)

        # 过期后答题页面也是进不去的
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_EXPIRED)


class TargetSurveyAnswerTest(TestCase):
    '''
    定向调查提交规则测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        self.client = Client()
        self.survey = Survey.objects.get(code='survey-target-01')  #网购客户满意度调查(定向)
        self.custList = self.survey.custList
        self.paper = self.survey.paper

        # 确认该调查为非定向调查
        self.assertIsNotNone(self.survey.custList)
        # 确定允许重复填写答案
        self.assertEqual(self.survey.resubmit, True)
        # 确定没有设置调查密码
        self.assertEqual(self.survey.password, '')
        # 确认是允许查看结果的
        self.assertTrue(self.survey.viewResult)

        # 相关的url链接
        self.answerUrl = reverse('survey:view.survey.answer.render', args=[self.survey.id])
        self.answerSubmitUrl = reverse('survey:view.survey.answer.submit')
        self.exportUrl = reverse('survey:view.survey.export', args=[self.survey.id])
        self.coverUrl = reverse('survey:view.survey.answer', args=[self.survey.id])
        self.viewUrl = reverse('survey:view.survey.viewResult', args=[self.survey.id])

        # 相关模板
        self.answerTemplate = 'survey/surveyAnswerAll.html'
        self.surveyLoginTemplate = 'survey/surveyLogin.html'
        self.messageTemplate = 'www/message.html'
        self.answeredTemplate = 'survey/surveyAnswered.html'
        self.viewRusultTemplate = 'survey/surveyViewResult.html'


        # 生成一个合法的答卷数据，供后面的过程提交使用
        data_valid = {}
        questionIdList = []
        data_valid['surveyId'] = self.survey.getIdSigned()
        for question in self.paper.question_set.all():
            questionIdList.append(question.getIdSigned())
            data_valid[question.getIdSigned()] = question.branch_set.all()[0].getIdSigned()
        data_valid['questionIdList'] = questionIdList
        self.data_valid = data_valid

    def test_enter_answer_page_no_phone(self):
        '''
        检查如果没有提供号码无法进入答题页面
        '''
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        # 检查是否直接转向答题模板
        self.assertEqual(self.surveyLoginTemplate, response.templates[0].name)


    def test_enter_answer_page_with_phone_not_in_list(self):
        '''
        检查如果提供一个错误的号码无法进入答题页面
        '''
        # 提交一个不相关的号码
        phone = '18900001111'
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        # 检查是否直接转向答题模板
        template = response.templates[0]
        self.assertEqual(template.name, self.messageTemplate)
        # 检查出错信息是否一致
        self.assertContains(response, RESULT_MESSAGE.PHONE_NOT_IN_CUSTLIST)


    def test_enter_answer_page_with_valid_phone(self):
        '''
        检查提供正确的号码可以进入答题页面
        '''
        # 先确认之前custTarget是没有记录的
        phone = self.custList.custListItem_set.all()[0].phone
        targetCustList = self.survey.targetCust_set.filter(phone=phone)
        self.assertEqual(len(targetCustList), 0)
        #提交数据到服务器
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        # 检查是否直接转向答题模板
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)
        # 确认数据
        survey = response.context['survey']
        self.assertEqual(self.survey.id, survey.id)
        paper = response.context['paper']
        self.assertEqual(self.survey.paper.id, paper.id)
        # 检查targetCust记录是否生成
        targetCustList = self.survey.targetCust_set.filter(phone=phone)
        self.assertEqual(len(targetCustList), 1)


    def test_answer_submit_success(self):
        '''
        测试提交问卷信息
        '''
        client = self.client
        sampleCount = self.survey.paper.sample_set.count()

        # 调用进入答卷页面生成targetCust记录
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        # 找到页面中的targetCustId
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "targetCustId"})
        targetCustId = input.get('value')
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCustId

        # 找到刚插入的targetCust记录
        #targetCust = self.survey.targetCust_set.filter(phone=phone)[0]
        #data_valid = copy.copy(self.data_valid)
        #data_valid['targetCustId'] = targetCust.getIdSigned()

        # 提交到服务器
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)

        # 检查提交的页面是否返回的是message页面
        self.assertEqual(response.templates[0].name, self.messageTemplate)

        # 检查是否返回成功信息
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 确认样本数量增加了一个
        self.assertEqual(self.survey.paper.sample_set.count(), sampleCount + 1)

        # 确认question数量和sample相同
        ## 获取最新添加的一个sample
        sample = self.survey.paper.sample_set.order_by('-createTime')[0]
        self.assertEqual(sample.sampleitem_set.count(), self.survey.paper.question_set.count())


    def test_answer_resubmit_with_same_phone(self):
        '''
        检查同一个号码的重复提交
        '''
        client = self.client

        # 调用进入答卷页面生成targetCust记录
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)

        # 找到刚插入的targetCust记录
        targetCust = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()

        # 第1此提交成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 第2次提交失败
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

        # 检查第2次进入页面也是失败的
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)


    def test_answer_resubmit_with_different_phone(self):
        '''
        模拟两个不同的号码在同一个客户端进行提交
        '''
        client = self.client

        # 模拟第1号码进入页面并生成提交数据
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        targetCust1 = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid1 = copy.copy(self.data_valid)
        data_valid1['targetCustId'] = targetCust1.getIdSigned()

        # 模拟第2号码进入页面并生成提交数据
        phone = self.custList.custListItem_set.all()[1].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        targetCust2 = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid2 = copy.copy(self.data_valid)
        data_valid2['targetCustId'] = targetCust2.getIdSigned()

        # 第1此提交成功
        response = client.post(self.answerSubmitUrl, data_valid1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 第2次提交也要成功
        response = client.post(self.answerSubmitUrl, data_valid2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)


    def test_answer_resubmit_same_phone_with_flag(self):
        '''
        测试使用重提交标志进行重新提交
        '''

        client = self.client

        # 调用进入答卷页面生成targetCust记录
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)

        # 找到刚插入的targetCust记录
        targetCust = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()
        data_valid['resubmit'] = True

        # 记录样本数量已便后面做数量比较
        count0 = self.survey.paper.sample_set.count()

        # 第1此提交成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 填写完问卷以后样本数量加1
        count1 = self.survey.paper.sample_set.count()
        self.assertEqual(count0 + 1, count1)

        # 增加了resubmit标识应该能提交成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 重填样本数量不能增加
        count2 = self.survey.paper.sample_set.count()
        self.assertEqual(count1, count2)

        # 没有增加重填标志无法进入页面返回answered
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)

        # 检查页面是否正常传递了phone信息
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "phone"})
        self.assertEqual(phone, input.get('value'))

        # 增加了resubmit标志，提交过后还能进入页面
        response = self.client.get(self.answerUrl, {'phone': phone, 'resubmit': True})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answerTemplate)

        # 测试是否提供上次填写的答案
        # 注意：这里已经假设了该问卷中全部都是单选题
        # 读取上次提交所有选项
        sample = self.survey.targetCust_set.get(phone=phone).sample_set.all()[0]
        soup = BeautifulSoup(response.content)
        signer = Signer()
        for sampleItem in sample.sampleitem_set.all():
            for branch in sampleItem.branch_set.all():
                input = soup.find(attrs={
                    "name": signer.sign(sampleItem.question.id),
                    'value': signer.sign(branch.id)
                })
                self.assertEqual(input.get('checked'), 'checked')

    def test_answer_resubmit_same_phone_with_flag_without_survey_flag(self):
        '''
        测试使用重提交标志，但调查本身不允许重复提交
        '''
        client = self.client

        # 修改resubmit为False
        self.survey.resubmit = False
        self.survey.save()

        # 调用进入答卷页面生成targetCust记录
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)

        # 找到刚插入的targetCust记录
        targetCust = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()
        data_valid['resubmit'] = True

        # 第1次提交成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 第2次提交即使增加了resubmit标志也无法成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

        # 增加了resubmit标志，提交过后还能进入页面
        response = self.client.get(self.answerUrl, {'phone': phone, 'resubmit': True})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)
        # 确认页面没有生成重填按钮
        #self.assertNotContains(response, u'重填')
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"id": "resubmitButton"})
        self.assertIsNone(input)

    def test_enter_page_with_password(self):
        '''
        测试进入页面时设置密码却没有提供的情况。
        '''
        client = self.client
        # 为调查设置密码
        self.survey.password = '123456'
        self.survey.save()

        # 读取清单中的一个号码
        phone = self.custList.custListItem_set.all()[0].phone

        # 没有给出密码不能进入页面
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)

        # 给出正确密码可以进入页面
        response = self.client.get(self.answerUrl, {'phone': phone, 'password': self.survey.password})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.templates[0].name, self.answerTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))

        # 给出错误密码也无法登陆
        response = self.client.get(self.answerUrl, {'phone': phone, 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)

    def test_submit_with_password(self):
        '''
        测试需要密码的调查的提交功能
        '''
        client = self.client
        # 为调查设置密码
        self.survey.password = '123456'
        self.survey.save()

        # 读取清单中的一个号码
        phone = self.custList.custListItem_set.all()[0].phone

        # 给出正确密码可以进入页面
        response = self.client.get(self.answerUrl, {'phone': phone, 'password': self.survey.password})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.templates[0].name, self.answerTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')

        # 找到刚插入的targetCust记录
        targetCust = self.survey.targetCust_set.filter(phone=phone)[0]

        # 在提交的数据中放入targetCustId但不放入密码信息
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()

        # 应该无法执行成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)

        # 在提交的数据中放入targetCustId和密码信息
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()
        data_valid['passwordEncoded'] = passwordEncoded

        # 提交数据并返回成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 再次提交返回重复提交页面，检查是否包含隐藏密码
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answeredTemplate)

        # 读取页面中的隐藏密码
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"name": "passwordEncoded"})
        passwordEncoded = input.get('value')
        self.assertTrue(check_password(self.survey.password, passwordEncoded))

        # 通过重填页面再次进入答题页面
        # 注意：在重填页面我们不想让用再次输入密码，又不能把密码明文出现在html返回结果中，
        # 所以只能在密码加密待答题页面对密码进行反向验证。
        response = self.client.get(
            self.answerUrl, {'resubmit': True, 'phone': phone, 'passwordEncoded': passwordEncoded})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.answerTemplate)


    def test_submit_expired_survey(self):
        '''
        测试过期后答题页面是进不去的
        '''

        # 修改调查使之过期
        self.survey.endTime = datetime.now()
        self.survey.save()

        # 读取清单中的一个号码
        phone = self.custList.custListItem_set.all()[0].phone
        # 尝试进入答题页面
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        # 返回调查已过期了
        template = response.templates[0]
        self.assertEqual(template.name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_EXPIRED)

        # 注意：这里无法测试提交，因为没有办法进入答题页面就没有办法生成targetCust记录，也就没有办法提交了。

    def test_enter_expired_survey_cover(self):
        '''
        尝试进入一个过期的调查的封面
        '''
        self.survey.endTime = datetime.now()
        self.survey.save()
        # 尝试进入调查封面
        response = self.client.get(self.coverUrl)
        self.assertEqual(response.status_code, 200)
        # 返回调查已过期了
        template = response.templates[0]
        self.assertEqual(template.name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_EXPIRED)


    def test_enter_view_result_page_protect(self):
        '''
        测试进入viewResult界面的保护措施
        '''
        client = self.client

        # 调用进入答卷页面生成targetCust记录
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)

        # 找到刚插入的targetCust记录
        targetCust = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()

        # 第1此提交成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 可以成功进入页面
        response = client.post(self.viewUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.viewRusultTemplate)

        # 修改调查属性禁止查看结果
        self.survey.viewResult = False
        self.survey.save()

        # 应该进不去了
        response = client.post(self.viewUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.VIEW_RESULT_IS_NOT_ALLOWED)


    def test_view_result_button_in_answered_page(self):
        '''
        测试在answered页面中按钮是否可以根据viewResult变化。
        '''
        client = self.client

        # 调用进入答卷页面生成targetCust记录
        phone = self.custList.custListItem_set.all()[0].phone
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)

        # 找到刚插入的targetCust记录
        targetCust = self.survey.targetCust_set.filter(phone=phone)[0]
        data_valid = copy.copy(self.data_valid)
        data_valid['targetCustId'] = targetCust.getIdSigned()

        # 第1此提交成功
        response = client.post(self.answerSubmitUrl, data_valid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, self.messageTemplate)
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 进入answered界面
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

        # 检查是否看见查看结果的按钮
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"id": "viewResultButton"})
        self.assertIsNotNone(input)

        # 修改调查属性禁止查看结果
        self.survey.viewResult = False
        self.survey.save()

        # 再次进入answered界面
        response = self.client.get(self.answerUrl, {'phone': phone})
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.answeredTemplate)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)

        # 应该要看不见按钮了
        soup = BeautifulSoup(response.content)
        input = soup.find(attrs={"id": "viewResultButton"})
        self.assertIsNone(input)


class StepSurveyAnswerTest(TestCase):
    '''
    分步调查的答题测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        # 登录
        self.client = Client()
        self.user = User.objects.get(code='duhan')
        loginForTest(self.client, self.user.phone, '123456')

        # 导入待测试的调查
        self.survey = Survey.objects.get(code='survey-targetless-step-01')  #网购客户满意度调查(非定向,分步)
        self.paper = self.survey.paper

        # 确认该调查为非定向调查
        self.assertIsNone(self.survey.custList)
        # 确定允许重复填写答案
        self.assertEqual(self.survey.resubmit, True)
        # 确定没有设置调查密码
        self.assertEqual(self.survey.password, '')
        # 确定是非匿名调查
        self.assertFalse(self.survey.anonymous)
        # 确认是允许查看结果的
        self.assertTrue(self.survey.viewResult)

        # 答题页面的url链接
        self.answerUrl = reverse('survey:view.survey.answer.render', args=[self.survey.id])
        self.answerSubmitUrl = reverse('survey:view.survey.answer.submit')


        # 导入问卷的4个问题
        self.question1 = self.paper.getQuestionSetInOrder()[0]
        self.question2 = self.paper.getQuestionSetInOrder()[1]
        self.question3 = self.paper.getQuestionSetInOrder()[2]
        self.question4 = self.paper.getQuestionSetInOrder()[3]

        # 构造一个数据：提交问题1的第1个选项，该选项nextQuestion为空表示直接进入下一题
        self.dataNext = {}
        self.dataNext['surveyId'] = self.survey.getIdSigned()
        self.dataNext['questionIdList'] = [self.question1.getIdSigned()]
        self.dataNext[self.question1.getIdSigned()] = self.question1.branch_set.all()[0].getIdSigned()

        # 构造一个数据：提交问题1的第2个选项,该选项nextQuestion为无效结束
        self.dataInValidEnd = {}
        self.dataInValidEnd['surveyId'] = self.survey.getIdSigned()
        self.dataInValidEnd['questionIdList'] = [self.question1.getIdSigned()]
        self.dataInValidEnd[self.question1.getIdSigned()] = self.question1.branch_set.all()[1].getIdSigned()

        #  构造一个数据：提交问题2的第1个选项,该选项nextQuestion为有效结束
        self.dataValidEnd = {}
        self.dataValidEnd['surveyId'] = self.survey.getIdSigned()
        self.dataValidEnd['questionIdList'] = [self.question2.getIdSigned()]
        self.dataValidEnd[self.question2.getIdSigned()] = self.question2.branch_set.all()[0].getIdSigned()

    def test_enter_answer_page(self):
        '''
        测试是否能正常进入页面
        '''
        #提交数据到服务器
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        # 检查显示的是否是第1题
        question = self.paper.getQuestionSetInOrder()[0]
        self.assertContains(response, question.text)


    def test_submit_question(self):
        '''
        测试提交一个问题，并进入下一题
        '''
        # 第1题的第1个选项，测试能够转向下一题
        response = self.client.post(self.answerSubmitUrl, self.dataNext)
        self.assertEqual(response.status_code, 200)

        # 检查是否进入下一题页面
        self.assertContains(response, self.question2.text)

        # 再次进入页面，检查显示的是否是第2题
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question2.text)

        # 获取样本对象
        sample = Sample.objects.get(session=self.client.session._session_key)
        # 确定调查是未完成状态
        self.assertFalse(sample.finished)

    def test_survey_invalid_end(self):
        '''
        测试问卷无效结束情况
        '''
        # 第1题的第2个选项，无效结束
        response = self.client.post(self.answerSubmitUrl, self.dataInValidEnd)
        self.assertEqual(response.status_code, 200)

        # 确认返回的是完成界面
        #print response
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 获取样本对象
        sample = Sample.objects.get(session=self.client.session._session_key)
        # 确定问卷时完成状态
        self.assertTrue(sample.finished)
        # 确定文本是一个无效样本
        self.assertFalse(sample.isValid)

        # 再次进入页面，提示已经回答过了
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)


    def test_survey_valid_end(self):
        '''
        测试问卷有效结束情况
        '''
        # 第1题的第1个选项，测试能够转向下一题
        response = self.client.post(self.answerSubmitUrl, self.dataNext)
        self.assertEqual(response.status_code, 200)

        # 检查是否进入下一题页面
        self.assertContains(response, self.question2.text)

        # 第2题的第1个选项，测试有效结束的情况
        response = self.client.post(self.answerSubmitUrl, self.dataValidEnd)
        self.assertEqual(response.status_code, 200)

        # 检查是否进入下一题页面
        self.assertContains(response, RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY)

        # 获取样本对象
        sample = Sample.objects.get(session=self.client.session._session_key)
        # 确定问卷时完成状态
        self.assertTrue(sample.finished)
        # 确定样本是一个有效样本
        self.assertTrue(sample.isValid)

        # 再次进入页面，提示已经回答过了
        response = self.client.get(self.answerUrl)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, RESULT_MESSAGE.ANSWERED_ALREADY)


    def test_survey_end(self):
        '''
        测试达到最后一题的情况
        '''
        pass


class TargetLessSurveyExportTest(TestCase):
    '''
    非定向调查的测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        self.client = Client()
        self.survey = Survey.objects.get(code='survey-targetless-01')  #网购客户满意度调查(非定向)
        self.exportUrl = reverse('survey:view.survey.export', args=[self.survey.id])
        # 登录
        self.user = User.objects.get(code='duhan')
        loginForTest(self.client, self.user.phone, '123456')

    def test_anonymous_export(self):
        '''
        测试匿名调查的导出是否含有用户信息
        '''
        client = self.client
        encoding = 'gb18030'
        ipColumn = u'IP'

        # 读取csv文件的内容
        response = client.post(self.exportUrl)
        buffer = BytesIO()
        for i in response.streaming_content:
            buffer.write(i)
        content = str(buffer.getvalue()).decode(encoding)

        # 非匿名调查可以查看到用户的信息
        self.assertIn(ipColumn, content)
        #self.assertIn

        # 将调查改为匿名调查
        self.survey.anonymous = True
        self.survey.save()

        # 再次读取csv文件的内容（此时已经是匿名调查）
        response = client.post(self.exportUrl)
        buffer = BytesIO()
        for i in response.streaming_content:
            buffer.write(i)
        content = str(buffer.getvalue()).decode(encoding)

        # 匿名调查信息都无法查到
        self.assertNotIn(ipColumn, content)


class TargetSurveyExportTest(TestCase):
    '''
    定向调查的测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        self.client = Client()
        self.survey = Survey.objects.get(code='survey-target-01')  #网购客户满意度调查(定向)
        self.exportUrl = reverse('survey:view.survey.export', args=[self.survey.id])
        # 登录
        self.user = User.objects.get(code='duhan')
        loginForTest(self.client, self.user.phone, '123456')

    def test_anonymous_export(self):
        '''
        测试匿名调查的导出是否含有用户信息
        '''
        client = self.client
        encoding = 'gb18030'
        nameColumn = u'用户姓名'
        phoneColumn = u'手机号码'
        ipColumn = u'IP'

        # 读取csv文件的内容
        response = client.post(self.exportUrl)
        buffer = BytesIO()
        for i in response.streaming_content:
            buffer.write(i)
        content = str(buffer.getvalue()).decode(encoding)

        # 非匿名调查可以查看到用户的信息
        self.assertIn(nameColumn, content)
        self.assertIn(phoneColumn, content)
        self.assertIn(ipColumn, content)
        #self.assertIn

        # 将调查改为匿名调查
        self.survey.anonymous = True
        self.survey.save()

        # 再次读取csv文件的内容（此时已经是匿名调查）
        response = client.post(self.exportUrl)
        buffer = BytesIO()
        for i in response.streaming_content:
            buffer.write(i)
        content = str(buffer.getvalue()).decode(encoding)

        # 匿名调查信息都无法查到
        self.assertNotIn(nameColumn, content)
        self.assertNotIn(phoneColumn, content)
        self.assertNotIn(ipColumn, content)


class SendSurveyToPhoneTest(TestCase):
    '''
    定向调查提交规则测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        # 准备提交的测试数据
        self.user = User.objects.get(code='duhan')
        self.user_other = User.objects.get(code='zhangjianhua')
        self.survey = self.user.surveyCreated_set.filter(state='A')[0]
        self.survey_others = self.user_other.surveyCreated_set.filter(state='A')[0]
        self.survey_del = self.user.surveyCreated_set.filter(state='P')[0]
        self.urlToPush = domain + reverse('survey:view.survey.answer.render', args=[self.survey.id])
        self.message = 'xxxllx%slkkejlls' % self.urlToPush
        self.message_bad = 'xxxllx%slkkejlls'
        self.data_valid = {'id': self.survey.getIdSigned(), 'message': self.message}
        self.data_bad_signature = {'id': self.survey.id, 'message': self.message}
        self.data_no_privilege = {'id': self.survey_others.getIdSigned(), 'message': self.message}
        self.data_bad_message = {'id': self.survey.getIdSigned(), 'message': self.message_bad}
        # 创建用户并且用其登陆
        self.client = Client()
        loginForTest(self.client, self.user.phone, '123456')
        self.serviceUrl = reverse('survey:service.survey.sendSurveyToPhone')

    def test_success(self):
        '''
        测试成功提交的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)

    def test_no_id(self):
        '''
        测试没有提交id的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, {})
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_ID)

    def test_bad_signature(self):
        '''
        测试数字签名不正确的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_signature)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.BAD_SAGNATURE)

    def test_no_privilege(self):
        '''
        测试没有权限的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_no_privilege)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NO_PRIVILEGE)

    def test_bad_message(self):
        '''
        测试url没有包含在短信内容中的情况
        '''
        client = self.client
        response = client.post(self.serviceUrl, self.data_bad_message)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.URL_NO_IN_MESSAGE)

    def test_frequently_send(self):
        client = self.client
        # 第一次调用应该是成功的
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.SUCCESS)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.SUCCESS)
        # 第二次调用应该失败
        response = client.post(self.serviceUrl, self.data_valid)
        result = json.loads(response.content)
        self.assertEquals(result['resultCode'], RESULT_CODE.ERROR)
        self.assertEquals(result['resultMessage'], RESULT_MESSAGE.NEED_WAIT)


class SurveyPublishTest(TestCase):
    '''
    定向调查提交规则测试
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        # 读取用户并登录
        self.user = User.objects.get(code='duhan')
        self.client = Client()
        loginForTest(self.client, self.user.phone, '123456')
        # 读取调查信息
        self.survey = Survey.objects.get(code='survey-target-01')  #网购客户满意度调查(定向)
        # 生成访问url
        self.serviceUrl = reverse('survey:view.survey.publish', args=[self.survey.id])
        # 定义相关模板
        self.publishTemplate = 'survey/surveyPublish.html'

    def test_publish_expired_survey(self):
        '''
        测试进入一个过期调查的发布页面
        '''
        # 尝试进入发布页面，可以进入页面且无提示信息
        response = self.client.get(self.serviceUrl)
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.publishTemplate)
        self.assertNotContains(response, RESULT_MESSAGE.SURVEY_EXPIRED)

        # 修改调查使之过期
        self.survey.endTime = datetime.now()
        self.survey.save()

        # 尝试进入发布页面，可以进入页面但又提示过期
        response = self.client.get(self.serviceUrl)
        self.assertEqual(response.status_code, 200)
        template = response.templates[0]
        self.assertEqual(template.name, self.publishTemplate)
        self.assertContains(response, RESULT_MESSAGE.SURVEY_EXPIRED)


class SurveyAddTest(TestCase):
    '''
    新增调查测试用例
    '''
    fixtures = ['initial_data.json']


    def setUp(self):
        # 为测试客户端登录
        self.user = User.objects.get(code='duhan')
        self.client = Client()
        loginForTest(self.client, self.user.phone, '123456')
        # 导入对应的
        self.paper = Paper.objects.get(code='paper-template-01', type='T')  #网购客户满意度调查(非定向)
        # 构造提交数据
        self.data_valid = {'paperId': self.paper.getIdSigned()}
        self.data_bad_signature = {'id': self.paper.id}
        # 准备url和模板
        self.url = reverse('survey:view.survey.add.action')
        self.publishTemplate = 'survey/surveyPublish.html'

    def test_success(self):
        '''
        测试提交成功的情况
        '''
        # 统计当前用户的调查数量
        surveyCount0 = self.user.surveyCreated_set.count()

        # 准备提交数据,viewResult默认值是True，这里特地设置成False测试设置可以生效
        data = copy.copy(self.data_valid)
        data['viewResult'] = False

        # 向服务器发出请求
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        # 检查对应的survey是否成功添加
        surveyCount1 = self.user.surveyCreated_set.count()
        self.assertEqual(surveyCount1, surveyCount0 + 1)

        # 提取添加的调查
        surveyList = self.user.surveyCreated_set.order_by('-createTime')
        survey = surveyList[0]
        self.assertFalse(survey.viewResult)











