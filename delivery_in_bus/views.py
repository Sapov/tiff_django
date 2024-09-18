from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse
from delivery_in_bus.forms import FormLoadImg, FormLoadImgStepTwo, FormLoadImgStepThree, FormLoadImgStepFour, \
    FormLoadImgCourier
from delivery_in_bus.models import OrdersDeliveryBus
from orders.models import Order


# Create your views here.
class ViewAllCompleteOrdersForBus(LoginRequiredMixin, ListView):
    '''Показать все ордера которые завершины и имеют статус доставка автобусом'''
    model = Order
    paginate_by = 6
    template_name = "delivery_in_bus/view_orders_for_courier.html"

    def get_queryset(self):
        return Order.objects.filter(status_id=5).filter(delivery_id=2).order_by("-id")


def render_instruction(request, order_id):
    if request.method == 'POST':
        # меняем статус заказа
        # начисляем баланс курьеру
        # Отправляем фото клиенту
        form = FormLoadImgCourier(request.POST, request.FILES)
        if form.is_valid():
            inst_order = Order.objects.get(id=order_id)
            itm = OrdersDeliveryBus()
            itm.order_id = inst_order
            itm.user = request.user
            itm.img_production = form.cleaned_data['img_production']
            itm.img_phone = form.cleaned_data['img_phone']
            itm.img_bus = form.cleaned_data['img_bus']
            itm.comments = form.cleaned_data['comments']
            itm.save()
            context = {'title': 'Фото упакованной продукции',
                       'order_id': order_id,
                       'item': itm,
                       }

            return render(request, 'delivery_in_bus/complete.html', context=context)
    else:
        form = FormLoadImgCourier()

        context = {'title': 'Инструкция для курьера',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)

    # context = {'order_id': order_id}
    # return render(request, template_name='delivery_in_bus/courier_instruction.html', context=context)


def load_img_phone(request, order_id):
    if request.method == 'POST':
        form = FormLoadImgStepTwo(request.POST, request.FILES)
        if form.is_valid():
            itm = OrdersDeliveryBus.objects.get(order_id=order_id)
            itm.img_phone = form.cleaned_data['img_phone']
            itm.save()
            form = FormLoadImgStepThree()
            context = {'title': 'Загрузи фото номера автобуса ',
                       'order_id': order_id,
                       'item': itm,
                       'form': form}

            return render(request, 'delivery_in_bus/view_img_phone.html', context=context)
    else:
        form = FormLoadImgStepTwo()

        context = {'title': 'Загрузи фото номера телефона водителя',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)


def load_img_number(request, order_id):
    print('load_img_number', )
    if request.method == 'POST':
        form = FormLoadImgStepThree(request.POST, request.FILES)
        if form.is_valid():
            itm = OrdersDeliveryBus.objects.get(order_id=order_id)
            itm.img_bus = form.cleaned_data['img_bus']
            itm.save()
            form = FormLoadImgStepFour()

            context = {'title': 'Добавь камментарии',
                       'order_id': order_id,
                       'item': itm,
                       'form': form}

            return render(request, 'delivery_in_bus/view_img_number.html', context=context)
    else:
        form = FormLoadImgStepThree()

        context = {'title': 'Загрузи фото номера автобуса',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)


def add_comment(request, order_id):
    if request.method == 'POST':
        form = FormLoadImgStepFour(request.POST)
        if form.is_valid():
            itm = OrdersDeliveryBus.objects.get(order_id=order_id)
            itm.comments = form.cleaned_data['comments']
            itm.save()
            context = {'title': 'Отгрузка завершена',
                       'order_id': order_id,
                       'item': itm}

            return render(request, 'delivery_in_bus/complete.html', context=context)
    else:
        form = FormLoadImgStepFour()

        context = {'title': 'Загрузи фото номера автобуса',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)


def complete(request, order_id):
    if request.method == 'POST':
        # меняем статус заказа
        # начисляем баланс курьеру
        # Отправляем фото клиенту
        form = FormLoadImgStepFour(request.POST)
        if form.is_valid():
            itm = OrdersDeliveryBus.objects.get(order_id=order_id)
            itm.comments = form.cleaned_data['comments']
            itm.save()
            context = {'title': 'Отгрузка завершена',
                       'order_id': order_id,
                       'item': itm}

            return render(request, 'delivery_in_bus/complete.html', context=context)
    else:
        form = FormLoadImgStepFour()

        context = {'title': 'Загрузи фото номера автобуса',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)


def courier_img(request, order_id):
    if request.method == 'POST':
        # меняем статус заказа
        # начисляем баланс курьеру
        # Отправляем фото клиенту
        form = FormLoadImgCourier(request.POST, request.FILES)
        if form.is_valid():
            inst_order = Order.objects.get(id=order_id)
            itm = OrdersDeliveryBus()
            itm.order_id = inst_order
            itm.user = request.user
            itm.img_production = form.cleaned_data['img_production']
            itm.img_phone = form.cleaned_data['img_phone']
            itm.img_bus = form.cleaned_data['img_bus']
            itm.comments = form.cleaned_data['comments']

            itm.save()
            context = {'title': 'Фото упакованной продукции',
                       'order_id': order_id,
                       'item': itm,
                       }

            return render(request, 'delivery_in_bus/complete.html', context=context)
    else:
        form = FormLoadImgCourier()

        context = {'title': 'Загрузка фото',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)
