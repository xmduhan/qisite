#-*- coding: utf-8 -*-

from survey.models import Survey, TargetCust, Sample, Question, Branch, SampleItem
from account.models import User
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.core.urlresolvers import reverse
from qisite.definitions import RESULT_MESSAGE
from django.core.signing import Signer, BadSignature
from django.db import transaction

#self.phone = request.REQUEST.get('phone')
#self.submitedSurveyList = request.session.get('submitedSurveyList', [])
#self.resubmit = request.REQUEST.get('resubmit', False)
#self.password = request.REQUEST.get('password')
#self.passwordEncoded = request.REQUEST.get('passwordEncoded', False)
#self.questionIdList = request.REQUEST.getlist('questionIdList')

def getAnonymousUser():
    return User.objects.get(code='anonymous')


class AuthController:
    '''
    鉴权器定义
    '''

    def __init__(self, controller):
        self.controller = controller
        self.request = controller.request

    def authCheck(self):
        return True

    def loginPage(self):
        pass

    def authErrorPage(self):
        pass


    def getAuthInfo(self):
        return {}


class SurveyAuthController(AuthController):
    '''
    调查鉴权器定义
    '''

    def __init__(self, controller):
        '''
        构造函数
        '''

        AuthController.__init__(self, controller)
        self.survey = self.controller.survey
        self.loginTemplate = 'survey/surveyLogin.html'
        self.__loadAuthInfo()
        self.__authErrorMessage = ''

    def __loadAuthInfo(self):
        '''
        导入鉴权相关信息
        '''

        # 处理显示控制器
        if type(self.controller) == SurveyRenderController:
            self.password = self.request.REQUEST.get('password')
            self.resubmit = self.request.REQUEST.get('resubmit', False)
            self.passwordEncoded = self.request.REQUEST.get('passwordEncoded', '')
            if not self.resubmit:
                #if True:
                # 重新提交的情况,其加密密码已经直接放在request中的passwordEncoded了
                self.passwordEncoded = make_password(self.password)

        # 处理提交控制器
        if type(self.controller) == SurveySubmitController:
            self.passwordEncoded = self.request.REQUEST.get('passwordEncoded', '')
            self.resubmit = self.request.REQUEST.get('resubmit', False)


    def authCheck(self):
        '''
        进入页面时的鉴权信息检查
        '''

        # 处理显示控制器
        if type(self.controller) == SurveyRenderController:

            # 调查没有设置密码则无需验证
            if not self.survey.password:
                return True

            # 重提情况的密码特殊处理
            if self.resubmit:
                # 重提交密码信息已经加密放在passwordEncoded中进行反向验证
                if check_password(self.survey.password, self.passwordEncoded):
                    return True
                else:
                    self.setAuthErrorMessage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)
                    return False

            # 非重提交情况下密码检查
            if self.survey.password == self.password:
                return True
            else:
                self.setAuthErrorMessage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)
                return False

        # 处理提交控制器
        if type(self.controller) == SurveySubmitController:

            # 调查没有设置密码
            if not self.survey.password:
                return True

            # 密码验证不正确
            if not check_password(self.survey.password, self.passwordEncoded):
                self.setAuthErrorMessage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)
                return False

            return True


    def getSample(self):
        '''
        获取上次用户回答的样本记录，用于样本信息的关联、再次读取和清空
        '''
        pass

    def setSample(self, sample):
        pass

    def getAuthInfo(self):
        '''
        获取鉴权信息提供给表单和重填控制页面，用于鉴权信息的传递
        '''
        # 这里无论显示还是提交的操作是一样的
        result = AuthController.getAuthInfo(self)
        if self.survey.password:
            result['passwordEncoded'] = self.passwordEncoded
        if self.resubmit:
            result['resubmit'] = self.resubmit
        return result

    def isAnswered(self):
        return False

    def loginPage(self):
        '''
        显示登录界面
        '''
        template = loader.get_template(self.loginTemplate)
        context = RequestContext(
            self.request, {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper})
        return HttpResponse(template.render(context))

    def authErrorPage(self):
        '''
        登陆错误
        '''
        if type(self.controller) == SurveyRenderController:
            if self.password != self.survey.password:
                #return self.controller.errorPage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)
                return self.controller.errorPage(self.getAuthErrorMessage())

        if type(self.controller) == SurveySubmitController:
            return self.controller.errorPage(self.getAuthErrorMessage())

    def getAuthErrorMessage(self):
        '''
        获取最后一次的鉴权检查的错误原因
        类似getLastError这样的过程，要先调用authCheck返回检查失败后在调用这个方法才能获取出错信息，否则返回可能无意义
        '''
        if self.__authErrorMessage == '':
            raise Exception(u'试图读取不存在的鉴权错误信息')
        return self.__authErrorMessage

    def setAuthErrorMessage(self, errorMessage):
        self.__authErrorMessage = errorMessage

    def onSubmitFinished(self):
        '''
        提交完成后的处理，主要是处理session相关信息
        '''
        pass

    pass


class TargetlessSurveyAuthController(SurveyAuthController):
    '''
    非定向调查的鉴权器
    '''

    def __init__(self, controller):
        SurveyAuthController.__init__(self, controller)
        self.__loadAuthInfo()

    def __loadAuthInfo(self):
        # 对于显示和提交操作相同
        self.submitedSurveyList = submitedSurveyList = self.request.session.get('submitedSurveyList', [])

    def isAnswered(self):
        '''
        判断是否答过
        通过检查surveyId是否在submitedSurveyList中
        '''
        return self.survey.id in self.submitedSurveyList

    def getSample(self):
        '''
        非定向调查通过session_key来获得上一次提交的sample记录
        '''
        session_key = self.request.session._session_key
        sampleList = self.survey.paper.sample_set.filter(session=session_key)
        if sampleList:
            return sampleList[0]
        else:
            return None

    def setSample(self, sample):
        '''
        鉴权信息保存在样本中
        '''
        # 非定向调查一样需要关联客户端信息(session)
        self.request.session['submitedSurveyList'] = self.submitedSurveyList
        self.request.session.save()  # 确保session记录是存在的
        sample.session = self.request.session._session_key
        sample.save()

    def authErrorPage(self):
        '''
        非定向调查的登录错误返回
        提示：非定向调查如果没有提供密码可能是第一次进入页面应该返回登陆界面，如果提供密码但错误返回密码错误提示。
        '''
        # 显示处理器
        if type(self.controller) == SurveyRenderController:
            if not self.password:
                return self.loginPage()
            return SurveyAuthController.authErrorPage(self)

        # 提交处理器
        if type(self.controller) == SurveySubmitController:
            return SurveyAuthController.authErrorPage(self)

    def onSubmitFinished(self):
        self.submitedSurveyList.append(self.survey.id)
        self.request.session['submitedSurveyList'] = self.submitedSurveyList

    pass


class TargetSurveyAuthController(SurveyAuthController):
    '''
    定向调查的鉴权器
    '''

    def __init__(self, controller):
        SurveyAuthController.__init__(self, controller)
        # 调用父类的保存登录信息过程
        self.phone = self.request.REQUEST.get('phone')
        self.targetCust = None  # initial in saveLoginInfo()
        self.__loadAuthInfo()

    def __loadAuthInfo(self):
        '''
        初始化鉴权相关信息
        '''
        # 显示处理器
        if type(self.controller) == SurveyRenderController:
            if self.isPhoneInList(self.phone):
                # 检查号码对应的targetCust记录是否已经生成，生成了就读取，没有生成就生成
                targetCustList = self.survey.targetCust_set.filter(phone=self.phone)
                if len(targetCustList) == 0:
                    custListItemList = self.survey.custList.custListItem_set.filter(phone=self.phone)
                    custListItem = custListItemList[0]
                    targetCust = TargetCust(
                        name=custListItem.name, phone=custListItem.phone, email=custListItem.email, survey=self.survey,
                        createBy=self.survey.createBy, modifyBy=self.survey.createBy,
                    )
                    targetCust.save()
                else:
                    targetCust = targetCustList[0]

                # 保存到对象变量中,以便后面可以访问
                self.targetCust = targetCust

        # 提交处理器
        if type(self.controller) == SurveySubmitController:
            self.targetCust = None
            targetCustIdSigned = self.request.REQUEST.get('targetCustId')
            if not targetCustIdSigned:
                #raise Exception(RESULT_MESSAGE.TARGET_SURVEY_NEED_CUSTLIST)  #定向调查需要提供客户清单
                self.__authErrorMessage = RESULT_MESSAGE.TARGET_SURVEY_NEED_CUSTLIST
                return
            # 验证目标清单的数字签名
            try:
                signer = Signer()
                targetCustId = signer.unsign(targetCustIdSigned)
            except:
                #raise Exception(RESULT_MESSAGE.BAD_SAGNATURE)  # 无效的数字签名
                self.__authErrorMessage = RESULT_MESSAGE.BAD_SAGNATURE
                return

            # 读取目标客户对象
            try:
                targetCust = TargetCust.objects.get(id=targetCustId)
            except:
                #raise Exception(RESULT_MESSAGE.CUSTLIST_OBJECT_NOT_EXIST)  # 所指定的客户清单的对象不存在
                self.__authErrorMessage = RESULT_MESSAGE.CUSTLIST_OBJECT_NOT_EXIST
                return

            # 检查目标清单和当前调查是否有关联，防止篡改
            if targetCust.survey != self.survey:
                #raise Exception(RESULT_MESSAGE.TARGETCUST_NOT_IN_SURVEY)
                self.__authErrorMessage = RESULT_MESSAGE.TARGETCUST_NOT_IN_SURVEY
                return

            # 将登录信息保存
            self.targetCust = targetCust

    def isPhoneInList(self, phone):
        '''
        检查号码是否在定向清单内
        '''
        custListItemList = self.survey.custList.custListItem_set.filter(phone=self.phone)
        if len(custListItemList) == 0:
            return False
        else:
            return True

    def authCheck(self):
        '''
        进入页面鉴权检查
        '''
        if type(self.controller) == SurveyRenderController:
            # 检查是否提供了号码
            if not self.phone:
                self.setAuthErrorMessage(RESULT_MESSAGE.NO_PHONE)
                return False

            # 检查号码是否在客户清单中
            if not self.isPhoneInList(self.phone):
                self.setAuthErrorMessage(RESULT_MESSAGE.PHONE_NOT_IN_CUSTLIST)
                return False

            # 执行父类的登录检查
            return SurveyAuthController.authCheck(self)

        if type(self.controller) == SurveySubmitController:
            if not self.targetCust:
                # 这里注意__authErrorMessage和父类的__authErrorMessage(通过setAuthErrorMessage访问)不是一回事
                self.setAuthErrorMessage(self.__authErrorMessage)
                return False

            # 执行父类的检查
            return SurveyAuthController.authCheck(self)


    def getAuthInfo(self):
        '''
        定向调查提交是需要提供的targetCust信息
        '''
        if type(self.controller) == SurveyRenderController:
            result = SurveyAuthController.getAuthInfo(self)
            result['targetCust'] = self.targetCust
            result['phone'] = self.phone
            return result

        if type(self.controller) == SurveySubmitController:
            result = SurveyAuthController.getAuthInfo(self)
            result['targetCust'] = self.targetCust
            result['phone'] = self.targetCust.phone
            return result

    def setSample(self, sample):
        '''
        鉴权信息保存在样本中
        '''
        sample.targetCust = self.targetCust
        sample.save()

    def getSample(self):
        '''
        获取鉴权信息对应的样本记录
        '''
        sampleList = self.targetCust.sample_set.filter(finished=True)
        if len(sampleList) != 0:
            return sampleList[0]
        else:
            return None

    def authErrorPage(self):
        '''
        定向调查的登录错误返回
        没有提供号码是第1次进入页面，不应提示错误
        '''

        # 检查是否提供了号码
        if self.getAuthErrorMessage() == RESULT_MESSAGE.NO_PHONE:
            return self.loginPage()

        # 检查号码是否在客户清单中
        #if not self.isPhoneInList(self.phone):
        #    return self.controller.errorPage(RESULT_MESSAGE.PHONE_NOT_IN_CUSTLIST)

        # 返回父类的错误登录页面
        return SurveyAuthController.authErrorPage(self)

    def isAnswered(self):
        '''
        定向调查检查是否已经答过题
        提示：通过号码检查targetCust记录
        '''
        #targetCustList = self.survey.targetCust_set.filter(phone=self.phone)
        #if len(targetCustList) == 0:
        #    return False
        #targetCust = targetCustList[0]
        #if targetCust.sample_set.count() == 0:
        #    return False
        #return True
        if not self.getSample():
            return False
        return True


    pass


class SurveyAnswerController:
    '''
    调查页面生成器
    '''

    def __init__(self, controller):
        self.controller = controller
        self.request = controller.request
        self.survey = self.controller.survey
        self.url = reverse('survey:view.survey.answer.render', args=[self.survey.id])
        self.answerAllTemplate = 'survey/surveyAnswerAll.html'
        self.answerStepTemplate = 'survey/surveyAnswerStep.html'

    def render(self):
        '''
        生成答题页面返回
        '''
        pass

    def submit(self):
        '''
        处理提交页面
        '''
        pass

    pass


class SurveyBulkAnswerController(SurveyAnswerController):
    '''
    非分步调查的页面生成器
    '''

    def answerPage(self, data):
        '''
        答题页面
        '''
        # 导入模板返回结果
        template = loader.get_template(self.answerAllTemplate)
        context = RequestContext(self.request, data)
        return HttpResponse(template.render(context))

    def render(self):
        '''
        生成答题页面返回
        '''
        # 准备进入页面的数据信息
        data = {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper}
        # 增加上次答题结果信息
        data['allBranchIdSelected'] = self.controller.getAllBranchSelected()
        # 增加鉴权信息
        submitAuthInfo = self.controller.authController.getAuthInfo()
        data = dict(data.items() + submitAuthInfo.items())
        # 返回页面
        return self.answerPage(data)

    @transaction.atomic()
    def __processSubmit(self):
        '''
        处理提交的操作
        '''
        # 答题处理
        user = getAnonymousUser()
        paper = self.survey.paper

        # 读取提交的问题列表
        questionIdList = self.request.REQUEST.getlist('questionIdList')

        # 检查提交问题数量是否和问卷定义一致
        if paper.question_set.count() != len(questionIdList):
            raise Exception(RESULT_MESSAGE.ANSWER_COUNT_DIFF_WITH_QUESTION)  # 提交问题的数量和问卷不一致

        # 添加样本对象
        ipAddress = self.controller.getClientIP()
        sample = Sample(user=user, ipAddress=ipAddress, paper=paper, createBy=user, modifyBy=user)

        # 关联鉴权信息
        authController = self.controller.getAuthController()
        if authController.isAnswered():
            authController.getSample().delete()
        authController.setSample(sample)

        # 保存样本
        sample.save()

        # 循环写入每一个选项的值
        for questionIdSigned in questionIdList:

            branchIdSinged = self.request.REQUEST.get(questionIdSigned)
            if not branchIdSinged:
                raise Exception(RESULT_MESSAGE.ANSWER_IS_MISSED_WHEN_REQUIRED)  # 问题答案没有完整填写

            # 检查数字签名
            try:
                signer = Signer()
                questionId = signer.unsign(questionIdSigned)
                branchId = signer.unsign(branchIdSinged)
            except:
                raise Exception(RESULT_MESSAGE.BAD_SAGNATURE)  # 数字签名无效

            # 读取问题对象
            try:
                question = Question.objects.get(id=questionId)
            except:
                raise Exception(RESULT_MESSAGE.QUESTION_OBJECT_NO_EXIST)  # 问题对象不存在

            # 选项对象不存在
            try:
                branch = Branch.objects.get(id=branchId)
            except:
                raise Exception(RESULT_MESSAGE.BRANCH_OBJECT_NO_EXIST)  # 选项对象不存在

            #
            if question.paper != paper:
                raise Exception(RESULT_MESSAGE.QUESTION_NOT_IN_PAPER)  #提交问题的问题此问卷无关

            branch_set = list(question.branch_set.all())
            if branch not in branch_set:
                raise Exception(RESULT_MESSAGE.BRANCH_NOT_IN_QUESTION)  #提交答案不在选项范围内

            # 将数据写到样本项信息中去
            sampleItem = SampleItem(
                question=question, content=None, score=0, sample=sample, createBy=user, modifyBy=user)
            sampleItem.save()
            sampleItem.branch_set.add(branch)
            sampleItem.save()

    def submit(self):
        '''
        处理答题提交数据(保存到数据库)
        '''
        # 尝试执行提交过程
        try:
            self.__processSubmit()
        except Exception as e:
            return self.controller.errorPage(unicode(e))

        # 通知鉴权器保存session信息
        self.controller.getAuthController().onSubmitFinished()

        # 返回成功
        returnUrl = reverse('survey:view.survey.answer', args=[self.survey.id])
        return self.controller.messagePage(u'完成', RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY, returnUrl)

    pass


class SurveyStepAnswerController(SurveyAnswerController):
    '''
    分步调查页面生成器
    '''

    def answerPage(self, data):
        '''
        答题页面
        '''
        # 导入模板返回结果
        template = loader.get_template(self.answerStepTemplate)
        context = RequestContext(self.request, data)
        return HttpResponse(template.render(context))

    def getNextQuestion(self):
        '''
        获取上次回答的题目,否则返回空
        '''
        # 检查上次答题的断点，从下一题开始答
        sample = self.controller.authController.getSample()
        if sample and sample.nextQuestion:
            return sample.nextQuestion
        else:
            # 如果没有上次答题断点信息，则从第1题开始答
            return self.survey.paper.getQuestionSetInOrder()[0]


    def render(self):
        '''
        生成答题页面返回
        '''
        # 读取上次答题的断点
        nextQuestion = self.getNextQuestion()
        # 准备进入页面的数据信息
        data = {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper,
                'question': nextQuestion}
        # 增加上次答题结果信息
        data['allBranchIdSelected'] = self.controller.getAllBranchSelected()
        # 增加鉴权信息
        submitAuthInfo = self.controller.authController.getAuthInfo()
        data = dict(data.items() + submitAuthInfo.items())
        # 返回页面
        return self.answerPage(data)


    @transaction.atomic()
    def __processSubmit(self):
        '''
        处理提交的操作
        '''
        # 读取http请求中的信息
        request = self.controller.request
        surveyId = request.REQUEST.getlist('surveyId')
        questionIdList = request.REQUEST.getlist('questionIdList')
        questionId = questionIdList[0]
        branchId = request.REQUEST[questionId]
        ret = {}
        ret['surveyId'] = surveyId
        ret['questionId'] = questionId
        ret['branchId'] = branchId

    def submit(self):
        '''
        处理答题提交数据(保存到数据库)
        '''
        request = self.controller.request
        questionIdList = request.REQUEST.getlist('questionIdList')
        _questionId = questionIdList[0]
        _branchId = request.REQUEST[_questionId]

        # 验证对象的数字签名
        try:
            signer = Signer()
            questionId = signer.unsign(_questionId)
            branchId = signer.unsign(_branchId)
        except Exception as e:
            return self.controller.errorPage(RESULT_MESSAGE.BAD_SAGNATURE)

        # 读取问题对象
        try:
            question = Question.objects.get(id=questionId)
        except:
            raise Exception(RESULT_MESSAGE.QUESTION_OBJECT_NO_EXIST)  # 问题对象不存在

        # 读取选项对象
        try:
            branch = Branch.objects.get(id=branchId)
        except:
            raise Exception(RESULT_MESSAGE.BRANCH_OBJECT_NO_EXIST)  # 选项对象不存在

        # 读取问题的数量
        paper = self.survey.paper
        questionCount = paper.question_set.count()

        # 尝试执行提交过程
        try:
            self.__processSubmit()
        except Exception as e:
            return self.controller.errorPage(unicode(e))

        # 通知鉴权器保存session信息
        authController = self.controller.getAuthController()
        authController.onSubmitFinished()
        sample = authController.getSample()
        if sample == None:
            user = getAnonymousUser()
            ipAddress = self.controller.getClientIP()
            sample = Sample(user=user, ipAddress=ipAddress, paper=paper, createBy=user, modifyBy=user, finished=False)
            sample.save()
            # 关联鉴权信息
            authController.setSample(sample)


        # 选项对应的nextQuestion为空(表示进入下一题)
        if branch.nextQuestion == None:
            if question.ord + 1 >= questionCount:
                # 返回成功
                returnUrl = reverse('survey:view.survey.answer', args=[self.survey.id])
                return self.controller.messagePage(u'完成', RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY, returnUrl)
            else:
                nextQuestion = paper.getQuestionSetInOrder()[question.ord + 1]
                # 准备进入页面的数据信息
                data = {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper,
                        'question': nextQuestion}
                # 增加上次答题结果信息
                data['allBranchIdSelected'] = self.controller.getAllBranchSelected()
                # 增加鉴权信息
                submitAuthInfo = self.controller.authController.getAuthInfo()
                data = dict(data.items() + submitAuthInfo.items())
                # 保存答题断点到sample对象
                sample.nextQuestion = nextQuestion
                sample.save()

                # 返回页面
                return self.answerPage(data)

        # 有效与无效结束
        if branch.nextQuestion.type in ( 'EndValid', 'EndInvalid'):

            # 设置样本为完成状态
            sample.finished = True

            # 判断是有效完成还是无效完成
            if branch.nextQuestion.type == 'EndValid':
                sample.isValid = True
            if branch.nextQuestion.type == 'EndInvalid':
                sample.isValid = False

            # 保存样本信息
            sample.save()

            # 返回成功
            returnUrl = reverse('survey:view.survey.answer', args=[self.survey.id])
            return self.controller.messagePage(u'完成', RESULT_MESSAGE.THANKS_FOR_ANSWER_SURVEY, returnUrl)


class ResponseController(object):
    '''
    html控制器
    '''

    def __init__(self, request):
        self.request = request
        # 获取客户端的ip地址信息
        self.ipAddress = self.request.META['REMOTE_ADDR']

    def getClientIP(self):
        return self.ipAddress

    def process(self):
        pass


class SurveyResponseController(ResponseController):
    '''
    调查(Survey)返回控制器
    '''

    def __init__(self, request, surveyId):
        ResponseController.__init__(self, request)
        self.survey = Survey.objects.get(id=surveyId)
        self.allBranchIdSelected = []
        self.__init__url()
        self.__init__AuthController()
        self.__init__AnswerController()

    def __init__url(self):
        '''
        初始化相关的url
        '''
        self.answeredTemplate = 'survey/surveyAnswered.html'
        self.messageTemplate = 'www/message.html'
        self.url = reverse('survey:view.survey.answer.render', args=[self.survey.id])

    def __init__AuthController(self):
        '''
        初始化鉴权控制器
        '''
        # 为控制器初始化鉴权器
        if self.survey.custList:
            self.authController = TargetSurveyAuthController(self)
        else:
            self.authController = TargetlessSurveyAuthController(self)

    def getAuthController(self):
        return self.authController

    def __init__AnswerController(self):
        '''
        初始化答题控制器
        '''
        # 为控制器初始化页面生成器
        if self.survey.paper.step:
            self.answerController = SurveyStepAnswerController(self)
        else:
            self.answerController = SurveyBulkAnswerController(self)

    def getAnswerController(self):
        return self.answerController


    def isExpired(self):
        '''
        检查是否调查是否过期了
        '''
        return self.survey.endTime <= datetime.now()

    def isActive(self):
        '''
        检查调查是否还在用
        '''
        return self.survey.state == 'A'

    def loadLastAnswer(self):
        '''
        读取上次答题的结果
        '''
        sample = self.authController.getSample()
        for sampleItem in sample.sampleitem_set.all():
            self.allBranchIdSelected.extend([branch.id for branch in sampleItem.branch_set.all()])


    def getAllBranchSelected(self):
        return self.allBranchIdSelected


    def messagePage(self, title, message, returnUrl):
        '''
        显示消息页面
        '''
        template = loader.get_template(self.messageTemplate)
        context = RequestContext(
            self.request, {'title': title, 'message': message, 'returnUrl': returnUrl})
        return HttpResponse(template.render(context))


    def errorPage(self, errorMessage=u'未知错误'):
        '''
        显示出错信息
        '''
        #template = loader.get_template(self.messageTemplate)
        #context = RequestContext(
        #    self.request, {'title': '出错', 'message': resultMessage, 'returnUrl': self.url})
        #return HttpResponse(template.render(context))
        return self.messagePage('出错', errorMessage, self.url)

    def answeredPage(self):
        '''
        提示已答过
        '''

        # 输送给answered页面的数据
        data = {'title': '提示', 'message': RESULT_MESSAGE.ANSWERED_ALREADY,
                'returnUrl': self.url, 'survey': self.survey}
        # 增加鉴权信息
        submitAuthInfo = self.authController.getAuthInfo()
        data = dict(data.items() + submitAuthInfo.items())
        # 导入模板返回结果
        template = loader.get_template(self.answeredTemplate)
        context = RequestContext(self.request, data)
        return HttpResponse(template.render(context))


class SurveyRenderController(SurveyResponseController):
    '''
    调查答题页面的生成控制器
    '''

    def __init__(self, request, surveyId):
        SurveyResponseController.__init__(self, request, surveyId)


    def process(self):
        '''
        生成页面主程序
        '''

        # 检查调查是否过期
        if self.isExpired():
            return self.errorPage(RESULT_MESSAGE.SURVEY_EXPIRED)

        # 检查是否提供登录信息
        authController = self.authController
        if not authController.authCheck():
            return authController.authErrorPage()

        # 获取sample对象信息
        sample = authController.getSample()

        # 检查是否已经回答过了
        if self.authController.isAnswered() and sample and sample.finished:
            if self.authController.resubmit and self.survey.resubmit:
                self.loadLastAnswer()
            else:
                return self.answeredPage()


        # 返回答题界面
        answerController = self.answerController
        return answerController.render()


class SurveySubmitController(SurveyResponseController):
    '''
    调查提交数据控制器
    '''

    def __init__(self, request, surveyId):
        SurveyResponseController.__init__(self, request, surveyId)


    def process(self):
        '''
        处理用户提交
        '''

        # 检查调查状态是否在用
        if not self.isActive():
            return self.errorPage(RESULT_MESSAGE.SURVEY_OBJECT_NOT_EXIST)

        # 检查是否过期
        if self.isExpired():
            return self.errorPage(RESULT_MESSAGE.SURVEY_EXPIRED)

        # 检查是否提供登录信息
        authController = self.authController
        if not authController.authCheck():
            return authController.authErrorPage()

        # 检查是否已经回答过了
        if self.authController.isAnswered():
            if not (self.authController.resubmit and self.survey.resubmit):
                return self.answeredPage()

        # 处理提交并返回结果
        answerController = self.answerController
        return answerController.submit()