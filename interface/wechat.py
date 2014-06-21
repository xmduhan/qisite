# Create your views here.

from django.http import HttpResponse


def service(request):
    print request.REQUEST
    return HttpResponse('')

