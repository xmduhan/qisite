# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def service(request):
    print request.REQUEST
    return HttpResponse('')

