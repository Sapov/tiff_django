import os

from django.http import JsonResponse

from lids.models import Lids
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from users.tasks import send_message_whatsapp
from .forms import UserLids, NewUserBanner
from .models import Lids, Interest


class AddLids(CreateView):
    model = Lids
    fields = ['lid_status', 'username', 'email', 'phone', 'channel', 'interest', 'interest_text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddLidsSiteUser(CreateView):
    model = Lids
    fields = ['username', 'email', 'phone', 'interest', 'interest_text']
    template_name = 'lids/user_site_order_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def add_user_lids(request):
    title = 'Новая заявка'
    template_name = 'lids/user_site_order_form.html'
    """ Пользователь отправил форму"""
    if request.method == 'POST':
        form = UserLids(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            cd['role'] = request.user
            print(cd)
            themas = cd['interest']
            Users = get_user_model()
            user = Users.objects.get(id=1)
            interest = Interest.objects.get(name=themas)
            username = cd['username']
            email = cd['email']
            phone = cd['phone']
            interest_text = cd['interest_text']
            Lids.objects.create(
                username=username,
                email=email,
                phone=phone,
                user=user,
                interest=interest,
                interest_text=interest_text)
            text = (f"Имя: {username}, \nТема: {themas}, \nИнформация: {interest_text}"
                    f"\nТелефон: {phone}, \nПочта: {email}")
            admin_phone = os.getenv('PHONE_NUMBER')
            send_message_whatsapp.delay(f'{admin_phone}', f'Новая заявка на сайте: \n{text}')

            try:
                return render(request, 'lids/thanks.html', {"form": form,
                                                            "title": title,
                                                            "results": cd,
                                                            }, )
            except:
                form.add_error(None, 'Ошибка расчета')
    else:
        form = UserLids()
        return render(request, template_name,
                      {"form": form, "title": title
                       })


def add_new_contact_user_banner(request):
    '''
    Тут обработать заявку с create_banner.html
    '''
    template_name = 'lids/create_banner.html'
    """ Пользователь отправил форму"""
    if request.method == 'POST':
        form = NewUserBanner(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            cd['role'] = request.user
            print(cd)
            Users = get_user_model()
            user = Users.objects.get(id=1)
            interest = Interest.objects.get(name='Баннера')
            username = cd['username']
            interest_text = cd['interest_text']
            email = cd['email']
            phone = cd['phone']
            Lids.objects.create(
                username=username,
                email=email,
                phone=phone,
                user=user,
                interest=interest,
                interest_text=interest_text)
            text = (f"Имя: {username}, \nТема: Баннера, \nИнформация: {interest_text}"
                    f"\nТелефон: {phone}, \nПочта: {email}")
            admin_phone = os.getenv('PHONE_NUMBER')
            # send_message_whatsapp.delay(f'{admin_phone}', f'Новая заявка на сайте: \n{text}')

            try:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Заказ принят в обработку',
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)

        # form = NewUserBanner()
        # return render(request, template_name,
        #               {"form": form,
        #                })


class DetailLids(DetailView):
    model = Lids
    template_name = 'lids/detail_lid.html'


class ListLids(ListView):
    model = Lids


class UpdateLids(UpdateView):
    model = Lids
    fields = ['lid_status', 'username',
              'phone', 'email',
              'channel', 'interest', 'interest_text']
    template_name_suffix = "_update_form"


class DeleteLids(DeleteView):
    model = Lids
    success_url = reverse_lazy("lids:list_lids")


class UpdateStatus(UpdateLids):
    fields = ['lid_status']
    template_name = 'lids/update_status.html'
