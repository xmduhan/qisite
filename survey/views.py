# Create your views here.

from django.http import HttpResponse
from django.template import Context,loader


def surveyEdit(request):
    template = loader.get_template('survey/surveyEdit.html')
    context = Context({})
    return HttpResponse(template.render(context))

def surveyList(request):
    template = loader.get_template('survey/surveyList.html')
    context = Context({})
    return HttpResponse(template.render(context))

def paperList(request):
    template = loader.get_template('survey/paperList.html')
    context = Context({})
    return HttpResponse(template.render(context))

def custList(request):
    template = loader.get_template('survey/custList.html')
    context = Context({})
    return HttpResponse(template.render(context))