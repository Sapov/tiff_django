from django.test import Client, TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class FileTemplateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='userTest')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_template_list_files(self):
        response = self.authorized_client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
