# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import View


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


def demo06(request):
    template = loader.get_template('demos/demo06.html')
    context = Context({})
    return HttpResponse(template.render(context))


def demo07(request):
    template = loader.get_template('demos/demo07.html')
    context = Context({})
    return HttpResponse(template.render(context))


class demo08(View):

    def get(self, request):
        # <view logic>
        return HttpResponse('result')