from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from http import HTTPStatus

from ..models import Organisation, Profile

User = get_user_model()


class TestDelivery(TestCase):

    def test_delivery_create(self):
        ''' Редирект пользователя с /account/delivery_list/'''
        response = self.client.get('/account/delivery_create/')
        self.assertEqual(response.status_code, 302)

    def test_delivery_update(self):
        ''' Редирект пользователя с /account/delivery_list/'''
        response = self.client.get('/account/delivery_update/1')
        self.assertEqual(response.status_code, 302)

    def test_delivery_delete(self):
        """ Редирект пользователя с /account/delivery_list/"""
        response = self.client.get('/account/delivery_delete/1')
        self.assertEqual(response.status_code, 302)

    def test_delivery_list(self):
        """ Редирект пользователя с /account/delivery_list/"""
        response = self.client.get('/account/delivery_list/')
        self.assertEqual(response.status_code, 302)

    # def test_delivery_list_templates(self):
    #     """ Редирект пользователя с /account/delivery_list/"""
    #     response = self.client.get('/account/delivery_list/')
    #
    #     self.assertTemplateUsed(response, 'delivery_list.html')


class TestOrganisation(TestCase):
    def test_add_organisation(self):
        response = self.client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'organisation_form.html')

    def test_list_organisation(self):
        response = self.client.get('/account/list_organisation/')
        a=1
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'organisation_list.html')

    def test_del_organisation(self):
        response = self.client.get('/account/delete_organisation_user/1')
        self.assertEqual(response.status_code, 302)

    def test_update_organisation(self):
        response = self.client.get('/account/update_organisation_user/1')
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'organisation_update_form.html')
