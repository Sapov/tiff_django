import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

from orders.tasks import feedback_mail
from .forms import Feedback
from .models import Menu, Info


def index(request):
    menu = Menu.objects.all()
    context = {"menu": menu}
    return render(request, template_name="info/index.html", context=context)


def banner(request):
    menu = Menu.objects.filter(pk=1)
    info = Info.objects.filter(pk=1)
    context = {"menu": menu, "info": info}
    return render(request, template_name="info/index.html", context=context)


def feedback(request):
    if request.method == "POST":
        form = Feedback(request.POST)
        if form.is_valid():
            date = {"response": "Мы в кратчайшие сроки с вами свяжемся!", "flag": 1}
            print(form.cleaned_data)
            cleaned_data = form.cleaned_data
            # отправояем письмо
            feedback_mail.delay(cleaned_data)

            return render(request, "info/feedback.html", date)  # изменение данных в БД

    else:
        form = Feedback()
        date = {"form": form, "title": "Обратная связь", "flag": 0}

        return render(request, "info/feedback.html", date)  # изменение данных в БД
