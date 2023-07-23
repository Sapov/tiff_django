from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from files.models import TypePrint
from django.views.generic.edit import CreateView, DeleteView
from .models import Organisation
from django.urls import reverse_lazy


@login_required
def dashboard(request):
    type_print = TypePrint.objects.order_by('id')
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'type_print': type_print})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя

            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class OrganisationCreateView(CreateView):
    '''
    добавление организации пользователем
    '''
    model = Organisation
    # fields = ['name']
    fields = ('__all__')
    success_url = '/account'


@login_required
def view_organisation_user(request):
    """Показать все организации пользователя"""
    organisation = Organisation.objects.filter(Contractor=request.user).order_by('id')
    return render(request, 'view_organisation.html', {'organisation': organisation, 'title': 'Мои организации'})


class OrganisationDeleteView(DeleteView):
    model = Organisation
    success_url = reverse_lazy('account:view_organisation_user')
