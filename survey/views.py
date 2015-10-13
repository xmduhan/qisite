#-*- coding: utf-8 -*-
# Create your views here.
from __future__ import division
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.template import Context, loader, RequestContext
from account.models import User
from models import *
from django.core.signing import Signer, BadSignature
from qisite.definitions import USER_SESSION_NAME
from django.core.paginator import Paginator
from qisite.utils import updateModelInstance
from django.core.urlresolvers import reverse
from django.db import transaction
import csv
from io import BytesIO
from qisite.definitions import RESULT_MESSAGE
import qrcode
from qrcode.image.pure import PymagingImage
from qisite.settings import domain
from django.db.models import Count
from django.contrib.auth.hashers import make_password, check_password
from controllers import SurveyRenderController, SurveySubmitController


def getCurrentUser(request):
    return request.session.get(USER_SESSION_NAME, None)


def getAnonymousUser():
    return User.objects.get(code='anonymous')


def surveyList(request, page=1):
    '''
        列出用户的调查
    '''
    perPage = 10
    # 确定page类型为整型
    if type(page) != int: page = int(page)
    # 读取用户
    user = getCurrentUser(request)
    surveyCreateSet = user.surveyCreated_set.filter(state='A').order_by('-modifyTime')
    paginator = Paginator(surveyCreateSet, perPage)
    # 对page的异常值进行处理
    if page < 1: page = 1
    if page > paginator.num_pages: page = paginator.num_pages
    # 读取当前分页数据
    thisPageSurveyList = paginator.page(page)
    # 通过模板生成返回内容
    baseUrl = reverse('survey:view.survey.list')
    template = loader.get_template('survey/surveyList.html')
    context = RequestContext(request,
                             {"surveyList": thisPageSurveyList, 'baseUrl': baseUrl, 'session': request.session})
    return HttpResponse(template.render(context))


def surveyEdit(request, surveyId):
    '''
        编辑调查
    '''
    surveyList = Survey.objects.filter(id=surveyId)
    if surveyList:
        survey = surveyList[0]
        template = loader.get_template('survey/surveyEdit.html')
        context = RequestContext(request, {'session': request.session, 'survey': survey})
        return HttpResponse(template.render(context))
    else:
        raise Http404


def paperList(request, page=1):
    '''
        列出用户的问卷
    '''
    perPage = 10
    # 确定page类型为整型
    if type(page) != int: page = int(page)
    # 读取用户
    user = getCurrentUser(request)
    # 读取用户所创建的问卷，并做分页处理
    paperCreateSet = user.paperCreated_set.filter(type='T').order_by('-modifyTime')
    paginator = Paginator(paperCreateSet, perPage)
    # 对page的异常值进行处理
    if page < 1: page = 1
    if page > paginator.num_pages: page = paginator.num_pages
    # 读取当前分页数据
    thisPagePaperList = paginator.page(page)
    # 通过模板生成返回内容
    baseUrl = reverse('survey:view.paper.list')
    template = loader.get_template('survey/paperList.html')
    context = RequestContext(request, {
        'paperList': thisPagePaperList,
        'baseUrl': baseUrl,
        'session': request.session
    })
    return HttpResponse(template.render(context))


def paperEdit(request, paperId):
    '''
        问卷编辑
    '''
    paperList = Paper.objects.filter(id=paperId)
    if paperList:
        paper = paperList[0]
        template = loader.get_template('survey/paperEdit.html')
        context = RequestContext(request, {'session': request.session, 'paper': paper})
        return HttpResponse(template.render(context))
    else:
        raise Http404


def paperPreview(request, paperId):
    '''
    问卷预览
    '''
    # 检查用户的登录状态
    user = getCurrentUser(request)
    if user == None:
        raise Exception(u'没有登录')

    # 读取问卷并创建实例
    paper = Paper.objects.get(id=paperId)
    if paper.createBy != user:
        raise Exception(u'没有权限预览该问卷')

    # 在系统系统管理源的名下创建一个调查
    admin = User.objects.get(code='admin')
    paperInstance = paper.createPaperInstance(admin)

    # 创建survey对象
    survey = Survey()
    survey.paper = paperInstance
    survey.createBy = admin
    survey.modifyBy = admin
    survey.save()

    # 返回答题界面
    return HttpResponseRedirect(reverse('survey:view.survey.answer', args=[survey.id]))


def surveyAdd(request, paperId):
    '''
        通过一个问卷发起一次调查
    '''
    # 检查用户是否存在
    user = getCurrentUser(request)
    if not user:
        raise Http404

    # 读取paper
    paperList = Paper.objects.filter(id=paperId)
    if not paperList:
        raise Http404
    paper = paperList[0]

    # 检查用户是否有权限使用这份问卷
    # 这里存在问题，因为我们应该允许用户引用系统用户创建的问卷，或者其他用户创造的共享问卷。
    # 该保护机制需要重新设计
    if paper.createBy != user:
        raise Http404

    # 读取用户可用的客户清单
    custListList = user.custListCreated_set.order_by('-modifyTime')

    # 导入模板
    template = loader.get_template('survey/surveyAdd.html')
    context = RequestContext(request, {'session': request.session, 'paper': paper, 'custListList': custListList})
    return HttpResponse(template.render(context))


@transaction.atomic
def surveyAddAction(request):
    #print request.REQUEST
    # 读取问卷标识
    paperIdSigned = request.REQUEST['paperId']

    # 验证问卷的数字签名
    sign = Signer()
    paperId = sign.unsign(paperIdSigned)
    #print  'paperId=', paperId

    # 检查用户的登录状态
    user = getCurrentUser(request)
    if user == None:
        raise Exception(u'没有登录')

    # 读取问卷并创建实例
    paper = Paper.objects.get(id=paperId)
    paperInstance = paper.createPaperInstance(user)
    paperInstance.survey

    # 创建survey对象
    survey = Survey()
    updateModelInstance(survey, request.REQUEST, tryUnsigned=True)
    survey.paper = paperInstance
    survey.createBy = user
    survey.modifyBy = user
    survey.save()

    # 设置文件到调查的反向连接，主要用于级联删除时使用
    paperInstance.survey = survey
    paperInstance.save()

    # 返回调查列表
    return HttpResponseRedirect(reverse('survey:view.survey.publish', args=[survey.id]))


def custListList(request, page=1):
    '''
        列出用户的客户清单
    '''
    perPage = 10
    # 确定page类型为整型
    if type(page) != int: page = int(page)
    # 读取用户
    user = getCurrentUser(request)
    # 读取用户所创建的问卷，并做分页处理
    custListCreateSet = user.custListCreated_set.all().order_by('-modifyTime')
    paginator = Paginator(custListCreateSet, perPage)
    # 对page的异常值进行处理
    if page < 1: page = 1
    if page > paginator.num_pages: page = paginator.num_pages
    # 读取当前分页数据
    thisPageCustListList = paginator.page(page)
    # 通过模板生成返回内容
    baseUrl = reverse('survey:view.custList.list')
    template = loader.get_template('survey/custListList.html')
    context = RequestContext(request, {
        "custListList": thisPageCustListList,
        'baseUrl': baseUrl,
        'session': request.session
    })
    return HttpResponse(template.render(context))


def custListEdit(request, custListId, page=1):
    '''
    客户清单编辑
    '''
    # 检查对象是否存在
    custListList = CustList.objects.filter(id=custListId)
    if not custListList:
        raise Http404
    custList = custListList[0]

    # 检查当前用户是否有权限查看该对象
    user = getCurrentUser(request)
    if custList.createBy != user:
        raise Http404

    # 读取数据并分页
    perPage = 10
    # 确定page类型为整型
    if type(page) != int: page = int(page)
    # 读取所有清单项并分页
    custListItemSet = custList.custListItem_set.order_by('-modifyTime')
    paginator = Paginator(custListItemSet, perPage)
    # 对page的异常值进行处理
    if page < 1: page = 1
    if page > paginator.num_pages: page = paginator.num_pages
    # 读取当前分页数据
    thisPageCustListItemList = paginator.page(page)

    baseUrl = reverse('survey:view.custList.edit', args=[custList.id]) + '/'
    #print 'baseUrl=', baseUrl

    # 读取模板生成页面
    template = loader.get_template('survey/custListEdit.html')
    context = RequestContext(
        request, {'session': request.session, 'custList': custList, 'custListItemList': thisPageCustListItemList,
                  'baseUrl': baseUrl})
    return HttpResponse(template.render(context))


def questionEdit(request, questionId):
    '''
        生成问题编辑DOM片段的view服务
    '''
    user = getCurrentUser(request)

    # 检查数字签名
    try:
        sign = Signer()
        questionIdUnsigned = sign.unsign(questionId)
    except BadSignature as bs:
        raise Http404

    # 根据id查询问题对象
    question = Question.objects.get(id=questionIdUnsigned)

    # 检查用户是否权限查看该对象
    if question.createBy != user:
        raise Http404

    # 返回数据
    template = loader.get_template('survey/question/questionEdit.html')
    context = RequestContext(request, {'question': question})
    return HttpResponse(template.render(context))


def surveyAnswer(request, surveyId):
    '''
    答题界面的统一入口
    '''
    # 读取调查对象
    surveyList = Survey.objects.filter(id=surveyId)
    if not surveyList:
        raise Http404
    survey = surveyList[0]

    # 检查调查是否过期
    if survey.endTime <= datetime.now():
        template = loader.get_template('www/message.html')
        context = RequestContext(
            request,
            {'title': '出错',
             'message': RESULT_MESSAGE.SURVEY_EXPIRED,
             'returnUrl': reverse('survey:view.survey.answer.render', args=[survey.id])}
        )
        return HttpResponse(template.render(context))

    # 返回问卷封面
    answerRenderUrl = reverse('survey:view.survey.answer.render', args=[surveyId])
    template = loader.get_template('survey/surveyCover.html')
    context = RequestContext(request, {'session': request.session, 'survey': survey, 'url': answerRenderUrl})
    return HttpResponse(template.render(context))


def surveyAnswerRender(request, surveyId):
    '''
    答题（一次性回答所有问题）

    '''
    # 读取survey对象
    surveyList = Survey.objects.filter(id=surveyId)
    if not surveyList:
        raise Http404
    survey = surveyList[0]

    # 调用显示控制器生成答题页面
    surveyRenderController = SurveyRenderController(request, survey.id)
    return surveyRenderController.process()


def surveyAnswerSubmit(request):
    '''
    问卷批量提交服务
    '''

    # 读取surveyId
    surveyIdSigned = request.REQUEST.get('surveyId')
    if not surveyIdSigned:
        #raise Exception(RESULT_MESSAGE.NO_SURVEY_ID)  # 没有提供调查对象
        template = loader.get_template('www/answerFinished.html')
        context = RequestContext(request, {'title': u'出错', 'message': RESULT_MESSAGE.NO_SURVEY_ID, 'returnUrl': '/'})
        return HttpResponse(template.render(context))

    # 对调查标识的数据签名进行检查
    try:
        signer = Signer()
        surveyId = signer.unsign(surveyIdSigned)
    except:
        #raise Exception(RESULT_MESSAGE.BAD_SAGNATURE)  # 无效的数字签名
        template = loader.get_template('www/answerFinished.html')
        context = RequestContext(request, {'title': u'出错', 'message': RESULT_MESSAGE.BAD_SAGNATURE, 'returnUrl': '/'})
        return HttpResponse(template.render(context))

    # 调用提交控制器生成处理数据，并生成返回结果
    surveySubmitController = SurveySubmitController(request, surveyId)
    return surveySubmitController.process()


def surveyExport(request, surveyId):
    '''
    将调查收集到的样本导出csv文件
    '''
    # 读取调查对象
    survey = Survey.objects.get(id=surveyId)

    # 检查权限
    user = getCurrentUser(request)
    if survey.createBy != user:
        raise Exception('没有权限查看')

    # 读取问卷相关信息
    paper = survey.paper
    questionList = list(paper.question_set.order_by('ord'))

    # 开始导出csv文件
    buffer = BytesIO()
    writer = csv.writer(buffer)
    encoding = 'gb18030'
    # 打印表头
    header = ['']

    if not survey.anonymous:
        header.append('IP')

    # 如果是定向调查需要增加用户信息
    if survey.custList and not survey.anonymous:
        header.extend([u'手机号码'.encode(encoding), u'用户姓名'.encode(encoding)])

    # 打印每一个问题
    for question in questionList:
        # 处理单选题
        if question.type == 'Single':
            questionText = ''.join([question.getNum(), question.text])
            questionTextEncoded = unicode(questionText).encode(encoding)
            header.append(questionTextEncoded)

        # 处理多选题
        if question.type == 'Multiple':
            questionText = ''.join([question.getNum(), question.text])
            for branch in question.getBranchSetInOrder():
                branchText = ''.join([branch.getNum(), branch.text])
                fullBranchText = '%s:%s' % ( questionText, branchText)
                fullBranchTextEncoded = unicode(fullBranchText).encode(encoding)
                header.append(fullBranchTextEncoded)

        # 处理问答题
        if question.type == 'Text':
            questionText = ''.join([question.getNum(), question.text])
            questionTextEncoded = unicode(questionText).encode(encoding)
            header.append(questionTextEncoded)

        # 处理评分题
        if question.type == 'Score':
            questionText = ''.join([question.getNum(), question.text])
            questionTextEncoded = unicode(questionText).encode(encoding)
            header.append(questionTextEncoded)

    writer.writerow(header)

    # 逐行打印数据
    for i, sample in enumerate(paper.sample_set.all()):
        row = [str(i + 1)]
        if not survey.anonymous:
            row.append(sample.ipAddress)
        # 如果是定向调查需要增加用户信息
        if survey.custList and not survey.anonymous:
            phone = unicode(sample.targetCust.phone).encode(encoding)
            name = unicode(sample.targetCust.name).encode(encoding)
            row.extend([phone, name])
        sampleItemDict = {sampleItem.question: sampleItem for sampleItem in sample.sampleitem_set.all()}
        for question in questionList:
            sampleItem = sampleItemDict.get(question)
            # 处理单选题
            if question.type == 'Single':
                if sampleItem:
                    branchTextList = []
                    for branch in sampleItem.branch_set.all():
                        branchText = ''.join([branch.getNum(), branch.text, ''])
                        branchTextList.append(branchText)
                    allBranchText = ' '.join(branchTextList)
                    allBranchTextEncoded = unicode(allBranchText).encode(encoding)
                    row.append(allBranchTextEncoded)
                else:
                    row.append('')
            # 处理多选题
            if question.type == 'Multiple':
                if sampleItem:
                    branchSelected = set(sampleItem.branch_set.all())
                else:
                    branchSelected = set()
                for branch in question.getBranchSetInOrder():
                    if branch in branchSelected:
                        row.append('1')
                    else:
                        row.append('0')
            # 处理问答题
            if question.type == 'Text':
                if sampleItem:
                    content = unicode(sampleItem.content).encode(encoding)
                    row.append(content)
                else:
                    row.append('')

            # 处理评分题
            if question.type == 'Score':
                if sampleItem:
                    row.append(str(int(sampleItem.score)))
                else:
                    row.append('')

        writer.writerow(row)
    response = StreamingHttpResponse(buffer.getvalue(), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="samples.csv"'
    return response


def surveyImageCode(request, surveyId):
    '''
    获取调查答题卷页面的url的二维码
    '''
    # 检查调查的代码是否存在
    surveyList = Survey.objects.filter(id=surveyId)
    if not surveyList:
        raise Http404
    survey = surveyList[0]

    # 检查当前用户是否有查看权限
    user = getCurrentUser(request)
    if survey.createBy != user:
        raise Http404

    # 拼接url

    url = '%s/%s' % (domain, reverse('survey:view.survey.answer.render', args=[survey.id]))

    # 将url转化为二维码形式返回客户端
    img = qrcode.make(url, image_factory=PymagingImage)
    buffer = BytesIO()
    img.save(buffer)
    response = StreamingHttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="test.png"'
    return response


def surveyPublish(request, surveyId):
    '''
    调查发布页面
    '''
    # 检查调查的代码是否存在
    surveyList = Survey.objects.filter(id=surveyId)
    if not surveyList:
        raise Http404
    survey = surveyList[0]

    resultMessage = ''
    if survey.endTime <= datetime.now():
        resultMessage = RESULT_MESSAGE.SURVEY_EXPIRED

    # 检查当前用户是否有查看权限
    user = getCurrentUser(request)
    if survey.createBy != user:
        raise Http404

    # 调用模板返回结果
    template = loader.get_template('survey/surveyPublish.html')
    context = RequestContext(
        request, {'session': request.session, 'survey': survey, 'domain': domain, 'resultMessage': resultMessage})
    return HttpResponse(template.render(context))


def surveyViewResult(request, surveyId):
    '''
    查看调查结果
    '''

    # 检查调查的代码是否存在
    surveyList = Survey.objects.filter(id=surveyId)
    if not surveyList:
        raise Http404
    survey = surveyList[0]

    if not survey.viewResult:
        template = loader.get_template('www/message.html')
        context = RequestContext(
            request,
            {'title': '出错',
             'message': RESULT_MESSAGE.VIEW_RESULT_IS_NOT_ALLOWED,
             'returnUrl': reverse('survey:view.survey.answer', args=[survey.id])}
        )
        return HttpResponse(template.render(context))
        #

    # 统计选线的选择次数
    branchList = Branch.objects.filter(question__paper=survey.paper).annotate(sampleitem_count=Count('sampleitem'))
    sampleCount = survey.paper.sample_set.count()
    branchSelCount = {}
    branchSelPct = {}
    for branch in branchList:
        branchSelCount[branch.id] = branch.sampleitem_count
        if sampleCount != 0:
            branchSelPct[branch.id] = branch.sampleitem_count / sampleCount * 100
        else:
            branchSelPct[branch.id] = 0
    # 调用模板返回结果
    template = loader.get_template('survey/surveyViewResult.html')
    context = RequestContext(
        request, {'session': request.session, 'survey': survey, 'paper': survey.paper,
                  'branchSelCount': branchSelCount, 'branchSelPct': branchSelPct})
    return HttpResponse(template.render(context))
