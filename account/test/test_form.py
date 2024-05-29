from django.test import TestCase

# Создайте ваши тесты здесь

import datetime
from django.utils import timezone
from account.forms import LoginForm, UserRegistrationForm


class LoginFormTest(TestCase):

    def test_login_form_field_label(self):
        form = LoginForm()
        self.assertTrue(
            form.fields['username'].label == None or form.fields['username'].label == 'username')

    def test_login_form_field_password_label(self):
        form = LoginForm()
        self.assertTrue(
            form.fields['password'].label == None or form.fields['password'].label == 'password')


class UserRegistrationFormTest(TestCase):

    def test_login_form_field_repet_password_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['password2'].label == None or form.fields['password2'].label == 'Repeat password')

    def test_login_form_field_password_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['password'].label == None or form.fields['password'].label == 'Password')

    #
    # def test_renew_form_date_today(self):
    #     date = datetime.date.today()
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertTrue(form.is_valid())
