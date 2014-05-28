# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader


def demo01(request):
    template = loader.get_template('demos/demo01.html')
    context = Context({})
    return HttpResponse(template.render(context))


def demo02(request):
    template = loader.get_template('demos/demo02.html')
    context = Context({})
    return HttpResponse(template.render(context))


def demo03(request):
    template = loader.get_template('demos/demo03.html')
    context = Context({})
    return HttpResponse(template.render(context))


def demo04(request):
    template = loader.get_template('demos/demo04.html')
    context = Context({})
    return HttpResponse(template.render(context))


def demo05(request):
    template = loader.get_template('demos/demo05.html')
    context = Context({})
    return HttpResponse(template.render(context))