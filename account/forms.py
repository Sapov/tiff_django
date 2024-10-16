from django import forms
# from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from .models import Organisation
from users.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


# ...
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", 'phone_number', 'whatsapp']


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ["name_full", "inn", "kpp", "address", ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'