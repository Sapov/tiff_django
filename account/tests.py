from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from django.test import TestCase

from account.models import Organisation


class TestAccount(TestCase):
    def test_add_organisation(self):
        response = self.client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'organisation_form.html')

    def test_list_organisation(self):
        response = self.client.get('/account/list_organisation/')
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'organisation_list.html')

    def test_del_organisation(self):
        response = self.client.get('/account/delete_organisation_user/1')
        self.assertEqual(response.status_code, 302)

    def test_update_organisation(self):
        response = self.client.get('/account/update_organisation_user/1')
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'organisation_update_form.html')

    # def test_model_Organisation_setUp(self):
    #     self.user = get_user_model().objects.create_user(
    #         username='testiser',
    #         email='test@mail.ru',
    #         password='secret',
    #     )

    # self.organisation = Organisation.objects.create(
    #     name_ul='Общество с ограниченной ответственностью Пароходная компания Юрия Майорова',
    #     address_ur='394000, г. Магадан, ул. Бывших Народных коммисаров, д. 17/8. строение 5, корпус 17, офис. 4557',
    #     address_post='000000, Московская область, г. Москва, ул. 2-я Хуторская, д. 54, строение 2 корпус 7,'
    #                  ' офис 55,',
    #     phone='+7 954 - 456 - 45 - 45',
    #     phone2='8(456) 456-46-45',
    #     email='poroplan@yandex.ru',
    #     inn='123456789',
    #     okpo='454566',
    #     published=True,
    # )

    # def test_setUp(self):
    #     self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
    #     self.organisation = Organisation.objects.create(
    #         Contractor=self.user,
    #         name_ul='Test Company',
    #         address_ur='Test Address',
    #         address_post='Test Post Address',
    #         phone='123456',
    #         email='test@example.com',
    #         inn='123456789012',
    #         kpp='123456789',
    #         okpo='123456789012',
    #     )


class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test@test.ru', password='12test12', email='test@test.ru')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test@test.ru', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
