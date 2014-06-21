# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def service(request):
    '''
        微信服务的中转器
    '''
    print request.REQUEST
    print request.POST
    return HttpResponse('')

