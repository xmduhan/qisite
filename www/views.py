# -*- coding: utf-8 -*-
# Create your views here.
from django.template import loader,Context
from django.http import HttpResponse

def index(request):
    template = loader.get_template('www/index.html')
    context = Context({})
    return HttpResponse(template.render(context))


def help(request):
    template = loader.get_template('www/help.html')
    context = Context({})
    return HttpResponse(template.render(context))