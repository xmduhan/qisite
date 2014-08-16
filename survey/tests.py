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
from services import RESULT_CODE, RESULT_MESSAGE

from account.models import User
import json, random, string
from django.contrib.auth.hashers import make_password
from account.tests import loginForTest, phoneForTest, passwordForTest
from django.core.signing import Signer
from django.db import transaction


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
            title='tsPaper', description='tsPaper.description', inOrder=True, lookBack=False, paging=False,
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


    def test_branch_getSystemPredefined(self):
        '''
        测试通过选项获取系统预定义出口（特殊问题）
        如果出现问题一般是数据缺失
        '''
        branch = Branch()
        questionList = branch.getSystemPredefined()
        self.assertEquals(len(questionList), 2)


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
    fixtures = ['initial_data.json']

    def setUp(self):
        setup_test_environment()
        self.user = User.objects.get(code='duhan')
        self.paper = Paper.objects.get(createBy=self.user, title=u'网购客户满意度调查')

    def test_createPaperInstance(self):
        newPaper = self.paper.createPaperInstance(self.user)
        #  检查对象是否是新创建的
        self.assertNotEqual(newPaper, self.paper)
        # 检查对象内容是否和原来一样
        self.assertEqual(newPaper.title,self.paper.title)
        # 检查所有的问题和选项都是新创建的
        for question in newPaper.question_set.all():
            self.assertNotIn(question, self.paper.question_set.all())
