from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):

    def test_create_user_with_role(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='teacher'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'teacher')
        self.assertTrue(user.check_password('testpass123'))
