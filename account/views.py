# Create your views here.

from django.template import loader,Context
from django.http import HttpResponse

def register(request):
    template = loader.get_template('account/register.html')
    context = Context({})
    return HttpResponse(template.render(context))