from http import HTTPStatus

from django.contrib.auth import get_user_model, authenticate

from django.test import TestCase

from account.models import Organisation


class TestAccount(TestCase):

    # def test_model_Organisation_setUp(self):
    #     self.user = get_user_model().objects.create_user(
    #         username='testiser',
    #         email='test@mail.ru',
    #         password='secret',
    #     )

    #
    #     self.organisation = Organisation.objects.create(
    #         name_ul='Общество с ограниченной ответственностью Пароходная компания Юрия Майорова',
    #         address_ur='394000, г. Магадан, ул. Бывших Народных коммисаров, д. 17/8. строение 5, корпус 17, офис. 4557',
    #         address_post='000000, Московская область, г. Москва, ул. 2-я Хуторская, д. 54, строение 2 корпус 7,'
    #                      ' офис 55,',
    #         phone='+7 954 - 456 - 45 - 45',
    #         phone2='8(456) 456-46-45',
    #         email='poroplan@yandex.ru',
    #         inn='123456789',
    #         okpo='454566',
    #         published=True,
    #     )

    def test_setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.organisation = Organisation.objects.create(
            Contractor=self.user,
            name_ul='Test Company',
            address_ur='Test Address',
            address_post='Test Post Address',
            phone='123456',
            email='test@example.com',
            inn='123456789012',
            kpp='123456789',
            okpo='123456789012',
        )


class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test@test.ru', password='12test12',
                                                         email='test@test.ru')
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


# class TestTemplates(TestCase):
#     # def setUp(self):
#     #     self.user = User.objects.create_user(
#     #         email='test@test.ru', password='pass1234', email_confirm=True)
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test@test.ru', password='12test12',
#                                                          email='test@test.ru')
#         self.user.save()
#
#         self.client.login(username='test@test.ru', password='pass1234')
#         # self.healht_data = baker.make(
#         #     HealthData, user=CustomUser.objects.get(id=self.user.id))
#         # self.parameters = baker.make(
#         #     Result, dashboard=self.healht_data, fat_percent='49 %, 3', bmi=20)
#         # self.url = reverse('cms:dashboard')
#         # self.resp = self.client.get(self.url)
#
#     def test_parameters_template(self):
#         self.response = self.client.get('/account/add_organisation/')
#
#         # self.assertEqual(self.response.status_code, 200)
#         self.assertTemplateUsed(self.response, 'organisation_form.html')
#         # self.assertContains(self.resp, 'form')
#         # self.assertContains(self.resp, 'measuring_system')
