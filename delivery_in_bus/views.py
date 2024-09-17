from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from delivery_in_bus.forms import FormLoadImg
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
    context = {'order_id': order_id}
    return render(request, template_name='delivery_in_bus/courier_instruction.html', context=context)


def load_img_production(request, order_id):
    if request.method == 'POST':
        form = FormLoadImg(request.POST, request.FILES)
        if form.is_valid():
            inst_order = Order.objects.get(id=order_id)
            OrdersDeliveryBus.objects.create(
                order_id=inst_order,
                user=request.user,
                img_production=form.cleaned_data['img_production'])
            context = {'title': 'Загрузи фото номера телефона водителя',
                       'order_id': order_id,
                       'form': form}

            return render(request, 'delivery_in_bus/step_2_load_img_phone.html', context=context)
    else:
        form = FormLoadImg()

        context = {'title': 'Загрузи фото упакованной продукции',
                   'order_id': order_id,
                   'form': form}
        return render(request, 'delivery_in_bus/ordersdeliverybus_form.html', context=context)

# class ImgProdCreateView(LoginRequiredMixin, CreateView):
#     model = OrdersDeliveryBus
#     form_class = FormLoadImg
#     fields = ['img_production']
#
# def form_valid(self, form):
#     form.instance.user = self.request.user
#     return super().form_valid(form)
