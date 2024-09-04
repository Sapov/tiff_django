# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
#
# from account.models import Organisation, Profile
# from ..models import Organisation, Profile
#
# User = get_user_model
#
#
# class TestModelProfile(TestCase):
#
#     def setUp(self):
#         self.guest_client = Client()
#         self.user = User.objects.create_user(username='auth')
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#         # Set up non-modified objects used by all
#         # test methods
#         Profile.objects.create(
#             user=User.objects.create(username='vasa'),
#             organisation=Organisation.objects.create(
#                 Contractor=self.user,
#                 name_ul='Test Company',
#                 address_ur='Test Address',
#                 address_post='Test Post Address',
#                 phone='123456',
#                 email='test@example.com',
#                 inn='123456789012',
#                 kpp='123456789',
#                 okpo='123456789012',
#             ),
#         )
#
#     def test_telegram_length(self):
#         profile = Profile.objects.get(id=1)
#         max_length = profile._meta.get_field('telegram').max_length
#         self.assertEqual(max_length, 15)
