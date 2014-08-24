#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.template import Context, loader, RequestContext
from account.models import User
from models import *
from django.core.signing import Signer, BadSignature
import services
from qisite.definitions import USER_SESSION_NAME
from django.core.paginator import Paginator
from qisite.utils import updateModelInstance
from django.core.urlresolvers import reverse
from django.db import transaction
import csv
from io import BytesIO


def getCurrentUser(request):
    #userList = User.objects.filter(name='杜涵')
    #if len(userList) > 0:
    #    return userList[0]
    #else:
    #    return None
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


def surveyAdd(request, paperId):
    '''
        通过一个问卷发起一次调查
    '''
    paperList = Paper.objects.filter(id=paperId)
    if paperList:
        paper = paperList[0]
        template = loader.get_template('survey/surveyAdd.html')
        context = RequestContext(request, {'session': request.session, 'paper': paper})
        return HttpResponse(template.render(context))
    else:
        raise Http404


@transaction.atomic
def surveyAddAction(request):
    # 读取问卷标识
    paperIdSigned = request.REQUEST['paperId']

    # 验证问卷的数字签名
    sign = Signer()
    paperId = sign.unsign(paperIdSigned)
    print  'paperId=', paperId

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
    updateModelInstance(survey, request.REQUEST)
    survey.paper = paperInstance
    survey.createBy = user
    survey.modifyBy = user
    survey.save()

    # 设置文件到调查的反向连接，主要用于级联删除时使用
    paperInstance.survey = survey
    paperInstance.save()

    # 返回调查列表
    return HttpResponseRedirect(reverse('survey:view.survey.list'))


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
    print 'baseUrl=', baseUrl

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


def answer(request, surveyId):
    '''
        编辑调查
    '''
    surveyList = Survey.objects.filter(id=surveyId)
    if surveyList:
        survey = surveyList[0]
        template = loader.get_template('survey/answer.html')
        context = RequestContext(request, {'session': request.session, 'survey': survey, 'paper': survey.paper})
        return HttpResponse(template.render(context))
    else:
        raise Http404


def answerSubmit(request):
    '''
    问卷一次型提交服务
    '''
    try:
        with transaction.atomic():
            # 尝试获取用户
            user = getCurrentUser(request)
            if not user:
                user = getAnonymousUser()

            # 获取客户端的地址信息
            ipAddress = request.META['REMOTE_ADDR']

            surveyIdSigned = request.REQUEST.get('surveyId')
            if not surveyIdSigned:
                raise Exception(u'缺少surveyId')

            signer = Signer()
            try:
                surveyId = signer.unsign(surveyIdSigned)
            except:
                raise Exception(u'surveyId:无效数字签名')

            try:
                survey = Survey.objects.get(id=surveyId, state='A')
            except:
                raise Exception(u'surveyId:对象不存在')

            paper = survey.paper
            questionIdList = request.REQUEST.getlist('questionIdList')

            if paper.question_set.count() != len(questionIdList):
                raise Exception(u'提交问题的数量和问卷不一致')

            # 添加样本对象
            sample = Sample(user=user, ipAddress=ipAddress, paper=paper, createBy=user, modifyBy=user)
            sample.save()

            for questionIdSigned in questionIdList:
                branchIdSinged = request.REQUEST.get(questionIdSigned)
                if not branchIdSinged:
                    raise Exception(u'请完整填写问卷中的所有问题')

                try:
                    questionId = signer.unsign(questionIdSigned)
                    branchId = signer.unsign(branchIdSinged)
                except:
                    raise Exception(u'无效数字签名')

                try:
                    print 'questionId=', questionId
                    print 'branchId=', branchId
                    question = Question.objects.get(id=questionId)
                    branch = Branch.objects.get(id=branchId)
                except:
                    raise Exception(u'数据已经不存在')

                if question.paper != paper:
                    raise Exception(u'提交问题的问题此问卷无关')

                branch_set = list(question.branch_set.all())
                if branch not in branch_set:
                    raise Exception(u'提交答案不在选项范围内')

                # 将数据写到样本项信息中去
                sampleItem = SampleItem(
                    question=question, content=None, score=0, sample=sample, createBy=user, modifyBy=user)
                sampleItem.save()
                sampleItem.branch_set.add(branch)
                sampleItem.save()

    except Exception as e:
        template = loader.get_template('survey/answerError.html')
        context = RequestContext(
            request, {'session': request.session, 'errorMessage': e.message, 'surveyId': surveyId})
        return HttpResponse(template.render(context))

    template = loader.get_template('survey/answerSubmit.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def sampleExport(request, surveyId):
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
    header = ['', 'IP']
    for question in questionList:
        questionText = ''.join([question.getNum(), question.text])
        questionTextEncoded = unicode(questionText).encode(encoding)
        header.append(questionTextEncoded)
    writer.writerow(header)

    # 逐行打印数据
    for i, sample in enumerate(paper.sample_set.all()):
        row = [str(i + 1), sample.ipAddress]
        sampleItemDict = {sampleItem.question: sampleItem for sampleItem in sample.sampleitem_set.all()}
        for question in questionList:
            sampleItem = sampleItemDict.get(question)
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
        writer.writerow(row)
    response = StreamingHttpResponse(buffer.getvalue(), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="samples.csv"'
    return response


