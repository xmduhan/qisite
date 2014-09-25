#-*- coding: utf-8 -*-

from survey.models import Survey
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

    def renderLoginPage(self):
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

    def makeEncodePassword(self):
        self.passwordEncoded = make_password(self.password)

    def isAnswered(self):
        return False


    def getLastSample(self):
        '''
        获取上次用户回答的样本记录
        '''
        pass


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


class TargetSurveyAuthenticator(SurveyAuthenticator):
    '''
    定向调查的鉴权器
    '''

    def __init__(self, controller):
        SurveyAuthenticator.__init__(self, controller)

    def isLogin(self):
        return Authenticator.isLogin(self)


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
        self.url = reverse('survey:view.survey.answer.all', args=[self.survey.id])
        self.allBranchIdSelected = []
        # 为控制器初始化鉴权器
        if self.survey.custList:
            self.authenticator = TargetSurveyAuthenticator(self)
        else:
            self.authenticator = NoTargetSurveyAuthenticator(self)


    def errorPage(self, resultMessage=u'未知错误'):
        '''
        显示出错信息
        '''
        template = loader.get_template('www/message.html')
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

    def loginPage(self):
        '''
        显示登录界面
        '''
        template = loader.get_template('survey/surveyLogin.html')
        context = RequestContext(
            self.request, {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper})
        return HttpResponse(template.render(context))

    def answerPage(self):
        '''
        进入答题页面
        '''
        template = loader.get_template('survey/surveyAnswerAll.html')
        context = RequestContext(
            self.request,
            {'session': self.request.session, 'survey': self.survey, 'paper': self.survey.paper,
             'resubmit': self.authenticator.resubmit, 'passwordEncoded': self.authenticator.passwordEncoded,
             'allBranchIdSelected': self.allBranchIdSelected})
        return HttpResponse(template.render(context))


    def isExpired(self):
        '''
        检查是否调查是否过期了
        '''
        return self.survey.endTime <= datetime.now()


    def rander(self):
        '''
        生成页面主程序
        '''
        # 检查调查是否过期
        if self.isExpired():
            return self.errorPage(RESULT_MESSAGE.SURVEY_EXPIRED)

        # 检查是否提供登录信息
        if not self.authenticator.isLogin():
            if not self.authenticator.password:
                return self.loginPage()
            else:
                return self.errorPage(RESULT_MESSAGE.SURVEY_PASSWORD_INVALID)
        self.authenticator.makeEncodePassword()

        # 检查是否已经回答过了
        if self.authenticator.isAnswered():
            if self.authenticator.resubmit and self.survey.resubmit:
                self.loadLastAnswer()
            else:
                return self.answeredPage()

        # 返回答题界面
        return self.answerPage()


    def answeredPage(self):
        '''
        提示已答过
        '''
        template = loader.get_template('survey/surveyAnswered.html')
        context = RequestContext(
            self.request,
            {'title': '提示',
             'message': RESULT_MESSAGE.ANSWERED_ALREADY,
             'returnUrl': reverse('survey:view.survey.answer.all', args=[self.survey.id]),
             'survey': self.survey, 'passwordEncoded': self.authenticator.passwordEncoded})
        return HttpResponse(template.render(context))

    def submit(self):
        pass



