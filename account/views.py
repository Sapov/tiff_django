from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

# from .models import Profile
from files.models import TypePrint
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from .models import Organisation, Profile
from django.urls import reverse_lazy


@login_required
def dashboard(request):
    type_print = TypePrint.objects.order_by("id")
    return render(
        request,
        "account/dashboard.html",
        {"section": "dashboard", "type_print": type_print},
    )


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return render(request, 'account/complite_edit.html')
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
    template_name = "organisation_list.html"
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
