from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from users.forms import UserCreationForm, AuthenticationForm
from users.utils import send_email_for_verify

User = get_user_model()


class MyLoginView(LoginView):
    form_class = AuthenticationForm


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class UsersCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = [
        'password',
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
        'password',
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
        # queryset = []
        queryset = User.objects.filter(email=self.request.user)
        #     q = User.objects.filter(user=self.request.user)
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