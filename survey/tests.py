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
        user = account.models.User()
        user.name = 'tsUser'
        user.phone = '1234567890'
        user.email = 'sample@example.com'
        user.save()
        self.tsUser = user

    def addPaper(self):
        paper = Paper()
        paper.title = 'tsPaper'
        paper.description = 'tsPaper.description'
        paper.inOrder = True
        paper.lookBack = False
        paper.style =  'P'
        paper.createBy = self.tsUser
        paper.modifyBy = self.tsUser
        paper.save()
        self.tsPaper = paper

    def addSurvey(self):
        survey = Survey()
        survey.paper = self.tsPaper     # 在没有问卷的情况下，是无法创建调查的
        survey.targetOnly = True
        survey.state = '?'
        survey.shared = False
        survey.viewResult = False
        survey.resubmit = False
        survey.passwd = ''
        #survey.ipLimit = 5
        #survey.ipLimit = 5
        survey.hardCost = 0
        survey.bonus = 0
        survey.fee = 0
        survey.validSampleLimit = 0
        survey.createBy = self.tsUser
        survey.modifyBy = self.tsUser
        survey.save()
        self.tsSurvey = survey

    def addSingleQuestion(self):
        # 增加一个单选题
        singleQuestion = Question()
        singleQuestion.type = 'Single'
        singleQuestion.contentLengh = 0
        singleQuestion.valueMin = 0
        singleQuestion.valueMin = 0
        singleQuestion.confused = False
        singleQuestion.nextQuestion = None
        singleQuestion.paper = self.tsPaper
        singleQuestion.createBy = self.tsUser
        singleQuestion.modifyBy = self.tsUser
        singleQuestion.save()
        self.tsSingleQuestion = singleQuestion
        # 增加单选题的题干
        singleStem = Stem()
        singleStem.text = '选择题'
        singleStem.question = singleQuestion
        singleStem.createBy = self.tsUser
        singleStem.modifyBy = self.tsUser
        singleStem.save()
        self.tsSingleStem = singleStem
        # 增加题支
        ## 1
        singleBranch1 = Branch()
        singleBranch1.text = '选项1'
        singleBranch1.ord = 1
        singleBranch1.nextQuestion = None
        singleBranch1.question = singleQuestion
        singleBranch1.createBy = self.tsUser
        singleBranch1.modifyBy = self.tsUser
        singleBranch1.save()
        ## 2
        singleBranch2 = Branch()
        singleBranch2.text = '选项2'
        singleBranch2.ord = 2
        singleBranch2.nextQuestion = None
        singleBranch2.question = singleQuestion
        singleBranch2.createBy = self.tsUser
        singleBranch2.modifyBy = self.tsUser
        singleBranch2.save()
        ## 3
        singleBranch3 = Branch()
        singleBranch3.text = '选项3'
        singleBranch3.ord = 3
        singleBranch3.nextQuestion = None
        singleBranch3.question = singleQuestion
        singleBranch3.createBy = self.tsUser
        singleBranch3.modifyBy = self.tsUser
        singleBranch3.save()
        ## 4
        singleBranch4 = Branch()
        singleBranch4.text = '选项4'
        singleBranch4.ord = 4
        singleBranch4.nextQuestion = None
        singleBranch4.question = singleQuestion
        singleBranch4.createBy = self.tsUser
        singleBranch4.modifyBy = self.tsUser
        singleBranch4.save()

    def addQuestions(self):
        self.addSingleQuestion()

    def addTargetCust(self):
        pass

    def addSamples(self):
        #  添加样本
        sample = Sample()
        sample.targetCust = None
        sample.user = None
        sample.ipAddress = '127.0.0.1'
        sample.macAddress = 'B8-70-F4-13-43-C6'
        sample.finished = True
        sample.isValid = True
        sample.paper = self.tsPaper
        sample.createBy = self.tsUser
        sample.modifyBy = self.tsUser
        sample.save()
        #  添加样本项
        sampleItem = SampleItem()
        sampleItem.question = self.tsSingleQuestion
        sampleItem.content = None


    def setUp(self):
        self.addUser()
        self.addPaper()
        self.addSurvey()
        self.addQuestions()
        self.addTargetCust()
        self.addSamples()

    def test_1(self):
        pass

