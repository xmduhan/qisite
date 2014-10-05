#-*- coding: utf-8 -*-

from survey.models import Survey, CustList, TargetCust
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.core.urlresolvers import reverse
from qisite.definitions import RESULT_MESSAGE
from django.core.signing import Signer, BadSignature

#self.phone = request.REQUEST.get('phone')
#self.submitedSurveyList = request.session.get('submitedSurveyList', [])
#self.resubmit = request.REQUEST.get('resubmit', False)
#self.password = request.REQUEST.get('password')
#self.passwordEncoded = request.REQUEST.get('passwordEncoded', False)
#self.questionIdList = request.REQUEST.getlist('questionIdList')

class AuthController:
    '''
    鉴权器定义
    '''

    def __init__(self, controller):
        self.controller = controller
        self.request = controller.request

    def randerAuthCheck(self):
        return True

    def loginPage(self):
        pass

    def loginErrorPage(self):
        pass

    def loadAuthInfo(self):
        pass


    def getSubmitAuthInfo(self):
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

    def __loadAuthInfo(self):
        # 鉴权相关信息
        self.password = self.request.REQUEST.get('password')
        self.resubmit = self.request.REQUEST.get('resubmit', False)
        self.passwordEncoded = self.request.REQUEST.get('passwordEncoded', False)

        if not self.resubmit:
            #if True:
            # 重新提交的情况,其加密密码已经直接放在request中的passwordEncoded了
            self.passwordEncoded = make_password(self.password)

    def randerAuthCheck(self):
        '''
        进入页面时的鉴权信息检查
        '''
        if self.survey.password:
            if not self.resubmit:
                return self.survey.password == self.password
            else:
                return check_password(self.survey.password, self.passwordEncoded)
        else:
            return True

    def submitAuthCheck(self):
        return check_password(self.survey.password, self.passwordEncoded)

    def getSample(self):
        '''
        获取上次用户回答的样本记录，用于样本信息的关联、再次读取和清空
        '''
        pass

    def setSample(self, sample):
        pass

    def getSubmitAuthInfo(self):
        '''
        获取鉴权信息提供给表单和重填控制页面，用于鉴权信息的传递
        '''
        result = AuthController.getSubmitAuthInfo(self)
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

    def loginErrorPage(self):
        '''
        登陆错误
        '''
        if self.password != self.survey.password:
            return self.controller.errorPage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)

    pass


class TargetlessSurveyAuthController(SurveyAuthController):
    '''
    非定向调查的鉴权器
    '''

    def __init__(self, controller):
        SurveyAuthController.__init__(self, controller)
        self.__loadAuthInfo()

    def __loadAuthInfo(self):
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

    def loginErrorPage(self):
        '''
        非定向调查的登录错误返回
        提示：非定向调查如果没有提供密码可能是第一次进入页面应该返回登陆界面，如果提供密码但错误返回密码错误提示。
        '''
        if not self.password:
            return self.loginPage()
        return SurveyAuthController.loginErrorPage(self)

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

    def isPhoneInList(self, phone):
        '''
        检查号码是否在定向清单内
        '''
        custListItemList = self.survey.custList.custListItem_set.filter(phone=self.phone)
        if len(custListItemList) == 0:
            return False
        else:
            return True

    def randerAuthCheck(self):
        '''
        进入页面鉴权检查
        '''
        # 检查是否提供了号码
        if not self.phone:
            return False

        # 检查号码是否在客户清单中
        if not self.isPhoneInList(self.phone):
            return False

        # 执行父类的登录检查
        return SurveyAuthController.randerAuthCheck(self)

    def submitAuthCheck(self):
        '''
        提交鉴权检查
        '''
        targetCustIdSigned = self.request.REQUEST.get('targetCustId')

    def getSubmitAuthInfo(self):
        '''
        定向调查提交是需要提供的targetCust信息
        '''
        result = SurveyAuthController.getSubmitAuthInfo(self)
        result['targetCust'] = self.targetCust
        result['phone'] = self.phone
        return result

    def setSample(self, sample):
        '''
        鉴权信息保存在样本中
        '''
        sample.targetCust = self.targetCust
        sample.save()

    def getSample(self):
        '''

        '''
        sampleList = self.targetCust.sample_set.all()
        if len(sampleList) != 0:
            return sampleList[0]
        else:
            return None

    def loginErrorPage(self):
        '''
        定向调查的登录错误返回
        提示：没有提供号码是第1次进入页面，不应提示错误
        '''

        # 检查是否提供了号码
        if not self.phone:
            return self.loginPage()

        # 检查号码是否在客户清单中
        if not self.isPhoneInList(self.phone):
            return self.controller.errorPage(RESULT_MESSAGE.PHONE_NOT_IN_CUSTLIST)

        # 返回父类的错误登录页面
        return SurveyAuthController.loginErrorPage(self)

    def isAnswered(self):
        '''
        定向调查检查是否已经答过题
        提示：通过号码检查targetCust记录
        '''
        targetCustList = self.survey.targetCust_set.filter(phone=self.phone)
        if len(targetCustList) == 0:
            return False
        targetCust = targetCustList[0]
        if targetCust.sample_set.count() == 0:
            return False
        return True

    pass


class SubmitController:
    '''
    生成提交的表单页面，并对表单进行处理
    '''

    def __init__(self, controller):
        self.controller = controller
        self.request = controller.request

    def render(self):
        pass

    def submit(self):
        pass


class SurveyAnswerController(SubmitController):
    '''
    调查页面生成器
    '''

    def __init__(self, controller):
        SubmitController.__init__(self, controller)
        self.survey = self.controller.survey
        self.url = reverse('survey:view.survey.answer.all', args=[self.survey.id])
        self.answerAllTemplate = 'survey/surveyAnswerAll.html'


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
        allBranchIdSelected = self.controller.getAllBranchSelected()
        data['allBranchIdSelected'] = allBranchIdSelected
        # 增加鉴权信息
        submitAuthInfo = self.controller.authController.getSubmitAuthInfo()
        data = dict(data.items() + submitAuthInfo.items())
        # 返回页面
        return self.answerPage(data)


class SurveyBulkAnswerController(SurveyAnswerController):
    '''
    非分步调查的页面生成器
    '''
    pass


class SurveyStepAnswerController(SurveyAnswerController):
    '''
    分步调查页面生成器
    '''
    pass


class ResponseController(object):
    '''
    html控制器
    '''

    def __init__(self, request):
        self.request = request
        # 获取客户端的ip地址信息
        self.ipAddress = self.request.META['REMOTE_ADDR']


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
        self.url = reverse('survey:view.survey.answer.all', args=[self.survey.id])

    def __init__AuthController(self):
        '''
        初始化鉴权控制器
        '''
        # 为控制器初始化鉴权器
        if self.survey.custList:
            self.authController = TargetSurveyAuthController(self)
        else:
            self.authController = TargetlessSurveyAuthController(self)


    def __init__AnswerController(self):
        '''
        初始化答题控制器
        '''
        # 为控制器初始化页面生成器
        if self.survey.paper.step:
            self.answerController = SurveyStepAnswerController(self)
        else:
            self.answerController = SurveyBulkAnswerController(self)


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

    def errorPage(self, resultMessage=u'未知错误'):
        '''
        显示出错信息
        '''
        template = loader.get_template(self.messageTemplate)
        context = RequestContext(
            self.request, {'title': '出错', 'message': resultMessage, 'returnUrl': self.url})
        return HttpResponse(template.render(context))


    def answeredPage(self):
        '''
        提示已答过
        '''

        # 输送给answered页面的数据
        data = {'title': '提示', 'message': RESULT_MESSAGE.ANSWERED_ALREADY,
                'returnUrl': self.url, 'survey': self.survey}
        # 增加鉴权信息
        submitAuthInfo = self.authController.getSubmitAuthInfo()
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
        if not authController.randerAuthCheck():
            return authController.loginErrorPage()

        # 检查是否已经回答过了
        if self.authController.isAnswered():
            if self.authController.resubmit and self.survey.resubmit:
                self.loadLastAnswer()
            else:
                return self.answeredPage()

        # 返回答题界面
        submitController = self.answerController
        return submitController.render()


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
        if not authController.submitAuthCheck():
            return authController.loginErrorPage()
