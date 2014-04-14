# coding=utf-8
# Create your views here.



from django.http import HttpResponseRedirect,HttpResponse
from django.template import Context, loader


def index(request):
    template = loader.get_template('home/index.html')
    context = Context({})
    return HttpResponse(template.render(context))   # 调用index.html模板
