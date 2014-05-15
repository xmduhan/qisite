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
        user = account.models.User(
            name='tsUser',
            phone='1234567890',
            email='sample@example.com'
        )
        user.save()
        self.tsUser = user

    def addPaper(self):
        paper = Paper(
            title='tsPaper',
            description='tsPaper.description',
            inOrder=True,
            lookBack=False,
            style='P',
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        paper.save()
        self.tsPaper = paper

    def addSurvey(self):
        survey = Survey(
            paper=self.tsPaper,  # 在没有问卷的情况下，是无法创建调查的
            targetOnly=True,
            state='?',
            shared=False,
            viewResult=False,
            resubmit=False,
            passwd='',
            #survey.ipLimit = 5
            #survey.ipLimit = 5
            hardCost=0,
            bonus=0,
            fee=0,
            validSampleLimit=0,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        survey.save()
        self.tsSurvey = survey

    def addSingleQuestion(self):
        # 增加一个单选题
        singleQuestion = Question(
            type='Single',
            contentLengh=0,
            valueMin=0,
            valueMax=0,
            confused=False,
            branchNumStyle='S1',
            nextQuestion=None,
            paper=self.tsPaper,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        singleQuestion.save()
        self.tsSingleQuestion = singleQuestion
        # 增加单选题的题干
        singleStem = Stem(
            text='选择题',
            question=singleQuestion,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        singleStem.save()
        self.tsSingleStem = singleStem
        # 增加题支
        ## 1
        singleBranch1 = Branch(
            text='选项1',
            ord=1,
            nextQuestion=None,
            question=singleQuestion,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        singleBranch1.save()
        self.tsSingleBranch1 = singleBranch1
        ## 2
        singleBranch2 = Branch(
            text='选项2',
            ord=2,
            nextQuestion=None,
            question=singleQuestion,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        singleBranch2.save()
        self.tsSingleBranch2 = singleBranch2
        ## 3
        singleBranch3 = Branch(
            text='选项3',
            ord=3,
            nextQuestion=None,
            question=singleQuestion,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        singleBranch3.save()
        self.tsSingleBranch3 = singleBranch3
        ## 4
        singleBranch4 = Branch(
            text='选项4',
            ord=4,
            nextQuestion=None,
            question=singleQuestion,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        singleBranch4.save()
        self.tsSingleBranch4 = singleBranch4

    def addQuestions(self):
        self.addSingleQuestion()

    def addTargetCust(self):
        targetCust = TargetCust(
            name = '用户1',
            phone = '1234567890',
            email = 'targetCust@example.com',
            token = 'XC65GXAG',
            survey=self.tsSurvey,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        targetCust.save()
        self.tsTargetCust = targetCust

    def addSamples(self):
        #  添加样本
        sample = Sample(
            targetCust=self.tsTargetCust,
            user=None,
            ipAddress='127.0.0.1',
            macAddress='B8-70-F4-13-43-C6',
            finished=True,
            isValid=True,
            paper=self.tsPaper,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        sample.save()
        #  添加样本项
        sampleItem = SampleItem(
            question=self.tsSingleQuestion,
            content=None,
            score=0,
            sample=sample,
            createBy=self.tsUser,
            modifyBy=self.tsUser
        )
        sampleItem.save()
        sampleItem.branch_set.add(self.tsSingleBranch3)
        sampleItem.save()


    def setUp(self):
        self.addUser()
        self.addPaper()
        self.addSurvey()
        self.addQuestions()
        self.addTargetCust()
        self.addSamples()

    def test_1(self):
        pass

