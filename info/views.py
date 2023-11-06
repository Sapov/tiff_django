from django.shortcuts import render

from .models import Menu, Info


def index(request):
    menu = Menu.objects.all()
    context = {'menu': menu}
    return render(request, template_name='info/index.html', context=context)


def banner(request):
    menu = Menu.objects.filter(pk=1)
    info = Info.objects.filter(pk=1)
    context = {'menu': menu, 'info': info}
    return render(request, template_name='info/index.html', context=context)
