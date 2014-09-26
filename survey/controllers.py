#-*- coding: utf-8 -*-

from survey.models import Survey, CustList, TargetCust
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.core.urlresolvers import reverse
from qisite.definitions import RESULT_MESSAGE


#self.phone = request.REQUEST.get('phone')
#self.submitedSurveyList = request.session.get('submitedSurveyList', [])
#self.resubmit = request.REQUEST.get('resubmit', False)
#self.password = request.REQUEST.get('password')
#self.passwordEncoded = request.REQUEST.get('passwordEncoded', False)
#self.questionIdList = request.REQUEST.getlist('questionIdList')

class Authenticator:
    '''
    鉴权器定义
    '''

    def __init__(self, controller):
        self.controller = controller
        self.request = controller.request

    def isLogin(self):
        return True

    def loginPage(self):
        pass

    def loginErrorPage(self):
        pass

    def saveLoginInfo(self):
        pass

    def getResubmitAuthInfo(self):
        pass


class SurveyAuthenticator(Authenticator):
    '''
    调查鉴权器定义
    '''

    def __init__(self, controller):
        Authenticator.__init__(self, controller)
        self.survey = self.controller.survey
        self.password = self.request.REQUEST.get('password')
        self.resubmit = self.request.REQUEST.get('resubmit', False)
        self.passwordEncoded = self.request.REQUEST.get('passwordEncoded', False)
        self.loginTemplate = 'survey/surveyLogin.html'

    def isLogin(self):
        '''
        检查是否已经登录过了
        '''
        if self.survey.password:
            if not self.resubmit:
                return self.survey.password == self.password
            else:
                return check_password(self.survey.password, self.passwordEncoded)
        else:
            return True

    def saveLoginInfo(self):
        if not self.resubmit:
            #if True:
            # 重新提交的情况,其加密密码已经直接放在request中的passwordEncoded了
            self.passwordEncoded = make_password(self.password)

    def getResubmitAuthInfo(self):
        result = {}
        if self.password:
            result['passwordEncoded'] = self.passwordEncoded
        return result

    def isAnswered(self):
        return False


    def getLastSample(self):
        '''
        获取上次用户回答的样本记录
        '''
        pass

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

        '''
        if self.password != self.survey.password:
            return self.controller.errorPage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)


class NoTargetSurveyAuthenticator(SurveyAuthenticator):
    '''
    非定向调查的鉴权器
    '''

    def __init__(self, controller):
        SurveyAuthenticator.__init__(self, controller)
        self.submitedSurveyList = submitedSurveyList = self.request.session.get('submitedSurveyList', [])


    def isAnswered(self):
        '''
        判断是否答过
        通过检查surveyId是否在submitedSurveyList中
        '''
        return self.survey.id in self.submitedSurveyList

    def getLastSample(self):
        '''
        非定向调查通过session_key来获得上一次提交的sample记录
        '''
        session_key = self.request.session._session_key
        sampleList = self.survey.paper.sample_set.filter(session=session_key)
        if sampleList:
            return sampleList[0]
        else:
            return None

    def loginErrorPage(self):
        '''
        非定向调查的登录错误返回
        提示：非定向调查如果没有提供密码可能是第一次进入页面应该返回
        '''
        if not self.password:
            return self.loginPage()
        return SurveyAuthenticator.loginErrorPage(self)


class TargetSurveyAuthenticator(SurveyAuthenticator):
    '''
    定向调查的鉴权器
    '''

    def __init__(self, controller):
        SurveyAuthenticator.__init__(self, controller)
        self.phone = self.request.REQUEST.get('phone')
        self.targetCust = None  # initial in saveLoginInfo()


    def isPhoneInList(self, phone):
        '''
        检查号码是否在定向清单内
        '''
        custListItemList = self.survey.custList.custListItem_set.filter(phone=self.phone)
        if len(custListItemList) == 0:
            return False
        else:
            return True


    def isLogin(self):
        '''

        '''
        # 检查是否提供了号码
        if not self.phone:
            return False

        # 检查号码是否在客户清单中
        if not self.isPhoneInList(self.phone):
            return False

        # 执行父类的登录检查
        return SurveyAuthenticator.isLogin(self)

    def saveLoginInfo(self):
        '''

        '''
        # 调用父类的保存登录信息过程
        SurveyAuthenticator.saveLoginInfo(self)

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

    def getResubmitAuthInfo(self):
        result = SurveyAuthenticator.getResubmitAuthInfo(self)

        return result


    def getLastSample(self):
        return self.targetCust.sample_set.all()[0]


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
        return SurveyAuthenticator.loginErrorPage(self)

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


class Generator:
    '''
    页面生成器基类
    '''

    def __init__(self, controller):
        self.controller = controller
        self.request = controller.request


class SurveyGenerator(Generator):
    '''
    调查页面生成器
    '''

    def __init__(self, controller):
        Generator.__init__(self, controller)
        self.survey = self.controller.survey
        self.url = reverse('survey:view.survey.answer.all', args=[self.survey.id])

        self.answerAllTemplate = 'survey/surveyAnswerAll.html'
        self.answeredTemplate = 'survey/surveyAnswered.html'


    def answerPage(self):
        '''
        进入答题页面
        '''
        authenticator = self.controller.authenticator
        allBranchIdSelected = self.controller.allBranchIdSelected
        template = loader.get_template(self.answerAllTemplate)
        context = RequestContext(
            self.request,
            {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper,
             'resubmit': authenticator.resubmit, 'passwordEncoded': authenticator.passwordEncoded,
             'allBranchIdSelected': allBranchIdSelected})
        return HttpResponse(template.render(context))


    def answeredPage(self):
        '''
        提示已答过
        '''
        authenticator = self.controller.authenticator
        template = loader.get_template(self.answeredTemplate)
        context = RequestContext(
            self.request,
            {'title': '提示',
             'message': RESULT_MESSAGE.ANSWERED_ALREADY,
             'returnUrl': self.url,
             'survey': self.survey, 'passwordEncoded': authenticator.passwordEncoded})
        return HttpResponse(template.render(context))


class AllSurveyGenerator(SurveyGenerator):
    '''
    非分步调查的页面生成器
    '''
    pass


class StepSurveyGenerator(SurveyGenerator):
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


class SurveyController(ResponseController):
    '''
    调查返回控制器
    '''

    def __init__(self, request, surveyId):
        ResponseController.__init__(self, request)
        self.survey = Survey.objects.get(id=surveyId)
        self.allBranchIdSelected = []
        # 为控制器初始化鉴权器
        if self.survey.custList:
            self.authenticator = TargetSurveyAuthenticator(self)
        else:
            self.authenticator = NoTargetSurveyAuthenticator(self)
        # 为控制器初始化页面生成器
        if self.survey.paper.step:
            self.generator = StepSurveyGenerator(self)
        else:
            self.generator = AllSurveyGenerator(self)

        self.messageTemplate = 'www/message.html'
        self.url = reverse('survey:view.survey.answer.all', args=[self.survey.id])

    def errorPage(self, resultMessage=u'未知错误'):
        '''
        显示出错信息
        '''
        template = loader.get_template(self.messageTemplate)
        context = RequestContext(
            self.request, {'title': '出错', 'message': resultMessage, 'returnUrl': self.url})
        return HttpResponse(template.render(context))

    def loadLastAnswer(self):
        '''
        读取上次答题的结果
        '''
        sample = self.authenticator.getLastSample()
        for sampleItem in sample.sampleitem_set.all():
            self.allBranchIdSelected.extend([branch.id for branch in sampleItem.branch_set.all()])

    def isExpired(self):
        '''
        检查是否调查是否过期了
        '''
        return self.survey.endTime <= datetime.now()

    def rander(self):
        '''
        生成页面主程序
        '''
        generator = self.generator
        # 检查调查是否过期
        if self.isExpired():
            return self.errorPage(RESULT_MESSAGE.SURVEY_EXPIRED)

        # 检查是否提供登录信息
        authenticator = self.authenticator
        if not authenticator.isLogin():
            return authenticator.loginErrorPage()
        authenticator.saveLoginInfo()

        # 检查是否已经回答过了
        if self.authenticator.isAnswered():
            if self.authenticator.resubmit and self.survey.resubmit:
                self.loadLastAnswer()
            else:
                return generator.answeredPage()

        # 返回答题界面
        return generator.answerPage()


    def submit(self):
        pass



