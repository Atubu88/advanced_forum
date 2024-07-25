from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTests(TestCase):

    def test_registration_view(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')

    def test_user_registration(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_with_existing_email(self):
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='TestPassword123')
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect, form should be re-rendered
        self.assertContains(response, 'Учетная запись с таким адресом электронной почты уже существует.')

class UserLoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='TestPassword123')

    def test_login_view(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вход')

    def test_user_login(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_invalid_login(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect, form should be re-rendered
        self.assertContains(response, 'Пожалуйста, введите правильное имя пользователя и пароль.')
