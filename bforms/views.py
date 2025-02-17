import os

from django.shortcuts import render
from bforms.forms import SaleBanner

from django.views.generic.edit import CreateView
from .models import SiteOrder
from django.urls import reverse


class SiteOrderCreateView(CreateView):
    model = SiteOrder
    fields = '__all__'


def sale_banner(request):
    title = 'Заявка на расчет баннера "Продам", "Сдам" или "Аренда"'
    if request.method == 'POST':
        form = SaleBanner(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            name_banner = form.cleaned_data['name_banner'][0]
            context = {'form': form,
                       'title': title,
                       'phone': form.cleaned_data['phone'],
                       'cdata': form.cleaned_data,

                       }
            return render(request, 'bforms/sale_banner.html', context)
    else:
        form = SaleBanner()
    return render(request, 'bforms/sale_banner.html', {'form': form, 'title': title})


def order_complete(request):
    # ----------''' Сообщение дминистратору'''--------------
    ''' успешная отправка письма В будущем - -Сообщение менеджеру типографии'''
    admin_phone = os.getenv('PHONE_NUMBER')
    from users.tasks import send_message_whatsapp
    send_message_whatsapp.delay(f'{admin_phone}', f'Новая заявка на сайте !')

    return render(request, 'bforms/order_complete.html')
