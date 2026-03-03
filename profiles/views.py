from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .forms import UserEditForm, OrganisationForm, ProfileEditForm

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from .models import Organisation, DeliveryAddress
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)
Users = get_user_model()


@login_required
def dashboard(request):
    """Вывод Заказов только авторизованного пользователя"""
    Orders = Order.objects.filter(user=request.user).order_by("-id")
    object_list = Order.objects.filter(status_id=5).filter(delivery_id=2).order_by("-id")
    logger.info(f"Orders:  {Orders}")

    paginator = Paginator(Orders, 2)
    if "page" in request.GET:
        page_num = request.GET.get("page")
    else:
        page_num = 1
    logger.info(f"page_NUM: {page_num}")
    page_obj = paginator.get_page(page_num)
    logger.info(f"page_NUM: {page_obj}")

    return render(
        request,
        "profiles/dashboard.html",
        {"Orders": Orders, 'object_list': object_list, "title": "Заказы", "page_obj": page_obj, "section": "dashboard"},
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        # profile_form = ProfileEditForm(
        #     instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
        return redirect('profile_list')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request,
        "users/edit_profile.html",
        {"user_form": user_form},
    )


class OrganisationCreateView(LoginRequiredMixin, CreateView):
    """
    добавление организации пользователем
    """

    model = Organisation
    fields = [
        "name_full",
        "inn",
        "kpp",
        "address",
        'bik_bank',
        'bank_name',
        'bank_account',
        'bankCorrAccount',
        "address_post",
        "phone",
        "email",
    ]
    success_url = reverse_lazy("profiles:list_organisation")

    # только для текущего юзера
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListOrganisation(LoginRequiredMixin, ListView):
    template_name = "profiles/organisation_list.html"
    model = Organisation
    paginate_by = 5

    def get_queryset(self):
        "организации только этого юзера"
        # queryset = []
        queryset = Organisation.objects.filter(user=self.request.user)
        return queryset


class OrganisationDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление организации"""
    model = Organisation
    success_url = reverse_lazy("profiles:list_organisation")


class OrganisationUpdateView(LoginRequiredMixin, UpdateView):
    """Редакторование организации"""

    model = Organisation
    fields = (
        "name_full",
        "inn",
        "kpp",
        'bank_name',
        'bik_bank',
        'bank_account',
        'bankCorrAccount',
        "address",
        "address_post",
        "phone",
        "email",
    )
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("profiles:list_organisation")



class DeliveryAddressListView(LoginRequiredMixin, ListView):
    template_name = "profiles/delivery_list.html"
    model = DeliveryAddress
    paginate_by = 5

    def get_queryset(self):
        "Адреса доставки только этого юзера"
        queryset = DeliveryAddress.objects.filter(user=self.request.user)
        return queryset




class DeliveryAddressDelete(LoginRequiredMixin, DeleteView):
    model = DeliveryAddress
    fields = "__all__"
    success_url = reverse_lazy("profiles:delivery_list")


def politics(request):
    return render(request, 'registration/politics.html')


def ya_pvz(request):
    return render(request, 'profiles/ya_pvz.html')





@login_required
@csrf_protect
def save_delivery_point(request):
    if request.method == 'POST':
        try:
            # Получаем данные из FormData
            point_data = {
                'point_id': request.POST.get('point_id'),
                'point_name': request.POST.get('point_name'),
                'full_address': request.POST.get('full_address'),
                'country': request.POST.get('country'),
                'city': request.POST.get('city'),
                'street': request.POST.get('street'),
                'house': request.POST.get('house'),
                'comment': request.POST.get('comment'),
                'latitude': request.POST.get('latitude'),
                'longitude': request.POST.get('longitude'),
                'postal_code': request.POST.get('postal_code'),
                'delivery_type': request.POST.get('delivery_type', 'pickup_point'),
                'selected_at': request.POST.get('selected_at'),
            }

            print(point_data)

            DeliveryAddress.objects.create(
                user=request.user,
                **point_data
            )
            # Возвращаем успешный ответ
            return JsonResponse({
                'status': 'success',
                'message': 'Заказ принят в обработку',
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Метод не разрешен'
    }, status=405)

