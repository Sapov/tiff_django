from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .forms import UserEditForm, ProfileEditForm, OrganisationForm

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
    Orders = Order.objects.filter(Contractor=request.user).order_by("-id")
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
        "account/dashboard.html",
        {"Orders": Orders, 'object_list': object_list, "title": "Заказы", "page_obj": page_obj, "section": "dashboard"},
    )


class ListProfile(LoginRequiredMixin, ListView):
    template_name = "account/profile_list.html"
    model = Users
    paginate_by = 5

    def get_queryset(self):
        "организации только этого юзера"
        # queryset = []
        queryset = Users.objects.filter(email=self.request.user)
        #     q = User.objects.filter(user=self.request.user)
        return queryset


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('account:list_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
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
        'bank_name',
        'bik_bank',
        'bank_account',
        'bankCorrAccount',
        "address",
        "address_post",
        "phone",
        "email",
    ]
    success_url = reverse_lazy("account:list_organisation")

    # только для текущего юзера
    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


class ListOrganisation(LoginRequiredMixin, ListView):
    template_name = "account/organisation_list.html"
    model = Organisation
    paginate_by = 5

    def get_queryset(self):
        "организации только этого юзера"
        # queryset = []
        queryset = Organisation.objects.filter(Contractor=self.request.user)
        return queryset


class OrganisationDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление организации"""
    model = Organisation
    success_url = reverse_lazy("account:list_organisation")


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
    success_url = reverse_lazy("account:list_organisation")


class DeliveryAddressCreateView(LoginRequiredMixin, CreateView):
    # from django.views.generic.edit import CreateView
    model = DeliveryAddress
    fields = [
        "delivery_method",
        "region",
        "city",
        "street",
        "house",
        "entrance",
        "floor",
        "flat",
        "first_name",
        "second_name",
        "phone",
    ]
    success_url = reverse_lazy("account:delivery_list")

    # только для текущего юзера
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeliveryAddressListView(LoginRequiredMixin, ListView):
    template_name = "account/delivery_list.html"
    model = DeliveryAddress
    paginate_by = 5

    def get_queryset(self):
        "Адреса доставки только этого юзера"
        queryset = DeliveryAddress.objects.filter(user=self.request.user)
        return queryset


class DeliveryAddressUpdate(LoginRequiredMixin, UpdateView):
    model = DeliveryAddress
    fields = ["region", "city", "street", "house", "delivery_method"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("account:delivery_list")


class DeliveryAddressDelete(LoginRequiredMixin, DeleteView):
    model = DeliveryAddress
    fields = "__all__"
    success_url = reverse_lazy("account:delivery_list")


class OrganisationCreateViewTest(LoginRequiredMixin, CreateView):
    """
    добавление организации пользователем
    """

    model = Organisation
    fields = [
        "name_full",
        "inn",
        "kpp",
        "address",
        'bank_name',
        'bik_bank',
        'bank_account',
        'bankCorrAccount',
        "address_post",
        "phone",
        "email",
    ]
    template_name = 'account/organisation_form_test_form.html'
    success_url = reverse_lazy("account:list_organisation")

    # только для текущего юзера
    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


def add_organisation(request):
    print(request.__dict__)
    if request.method == 'POST':
        form = OrganisationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect("account:list_organisation")
    else:
        form = OrganisationForm()
    return render(request, 'account/organisation_form_test_form.html', {'form': form})
