# -*- coding: utf-8 -*-
# Create your views here.
from django.template import loader,Context,RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


def index(request):
    template = loader.get_template('www/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def help(request):
    template = loader.get_template('www/help.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
