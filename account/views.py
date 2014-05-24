# Create your views here.

from django.template import loader,Context,RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


def register(request):
    template = loader.get_template('account/register.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def login(request):

    phone = request['phone']
    password = request['password']
    template = loader.get_template('account/login.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))