from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

# from .models import Profile
from files.models import TypePrint
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from .models import Organisation, Profile, Delivery, DeliveryAddress
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User

Users = get_user_model()


@login_required
def dashboard(request):
    return render(
        request,
        "account/dashboard.html",
        {"section": "dashboard"},
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
        "name_ul",
        "inn",
        "kpp",
        "okpo",
        "address_ur",
        "address_post",
        "phone",
        "phone2",
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
        "name_ul",
        "inn",
        "kpp",
        "okpo",
        "address_ur",
        "address_post",
        "phone",
        "phone2",
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
    template_name = "delivery_list.html"
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
