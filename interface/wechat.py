#-*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def service(request):
    '''
        微信服务的中转器
    '''
    #request = HttpRequest()
    print '------1--------'
    print request.REQUEST
    print '------2--------'
    print request.POST
    print '------3--------'
    print request.body
    print '------4--------'
    return HttpResponse('ok')