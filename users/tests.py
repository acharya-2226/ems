from django.test import TestCase
from .models import CustomUser


class CustomUserTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))
