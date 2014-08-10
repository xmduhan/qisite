# -*- coding: utf-8 -*-
# Create your views here.
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse


def index(request):
    template = loader.get_template('www/index.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def help(request):
    template = loader.get_template('www/help.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def confirmDialog(request):
    template = loader.get_template('www/dialog/confirmDialog.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))


def messageDialog(request):
    template = loader.get_template('www/dialog/messageDialog.html')
    context = RequestContext(request, {'session': request.session})
    return HttpResponse(template.render(context))



