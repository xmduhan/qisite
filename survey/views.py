#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from account.models import User


def getCurrent():
    userList = User.objects.filter(name='杜涵')
    if len(userList) > 0:
        return userList[0]
    else:
        return None


def surveyEdit(request):
    template = loader.get_template('survey/surveyEdit.html')
    context = Context({})
    return HttpResponse(template.render(context))


def surveyList(request):
    user = getCurrent()
    surveyList = user.surveyCreated_set.all()
    #surveyList = user.surveyCreated_set.filter(state = 'P')
    template = loader.get_template('survey/surveyList.html')
    context = Context({"surveyList": surveyList})
    return HttpResponse(template.render(context))


def paperList(request):
    user = getCurrent()
    paperList = user.paperCreated_set.all()
    template = loader.get_template('survey/paperList.html')
    context = Context({"paperList": paperList})
    return HttpResponse(template.render(context))


def custListList(request):
    user = getCurrent()
    custListList = user.custListCreated_set.all()
    template = loader.get_template('survey/custListList.html')
    context = Context({'custListList': custListList})
    return HttpResponse(template.render(context))