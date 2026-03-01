from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

User = get_user_model()


class UsersCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = [
        'email',
        'username',
        'last_name',
        'phone_number',
    ]
    success_url = reverse_lazy("users_list")


class UserListsView(LoginRequiredMixin, ListView):
    template_name = "users/users_list.html"
    model = User


class UserUpdateLIst(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        'email',
        'username',
        'last_name',
        'phone_number'
    ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('users_list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users_list')


class ListProfile(LoginRequiredMixin, ListView):
    template_name = "users/profile_list.html"
    model = User
    paginate_by = 5

    def get_queryset(self):
        "организации только этого юзера"
        queryset = User.objects.filter(email=self.request.user)
        return queryset


class ProfileUpdateLIst(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'phone_number'
    ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('profile_list')


from .forms import DesignerSignUpForm


class DesignerSignUpView(CreateView):
    model = User
    form_class = DesignerSignUpForm
    template_name = 'registration/designer_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'designer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profiles:dashboard')  # Замените 'home' на ваш URL
