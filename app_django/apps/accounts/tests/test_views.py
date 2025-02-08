from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.cache import cache
from django.utils import timezone
from apps.accounts.models import Profile


class ProfileViewTest(TestCase):

    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.profile = Profile.objects.create(user=self.user, slug='testuser-slug')
        self.client.login(username='testuser', password='testpassword123')

    def test_profile_detail_view(self):
        """Тест просмотра профиля"""
        response = self.client.get(reverse('profile_detail', kwargs={'slug': self.profile.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_detail.html')
        self.assertContains(response, f'Профиль пользователя: {self.user.username}')

    def test_profile_update_view(self):
        """Тест редактирования профиля"""
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

        # Обновляем данные профиля
        response = self.client.post(reverse('profile_edit'), {
            'bio': 'Updated bio',
            'birth_date': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешного сохранения
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')


class AuthTest(TestCase):

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        response = self.client.post(reverse('user_register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Редирект на главную страницу
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """Тест авторизации пользователя"""
        user = User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Редирект на `home`
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_user_logout(self):
        """Тест выхода из системы"""
        user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)  # Редирект на `home`
        self.assertFalse(get_user(self.client).is_authenticated)


class PasswordChangeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpassword123')
        self.client.login(username='testuser', password='oldpassword123')

    def test_password_change(self):
        """Тест смены пароля"""
        response = self.client.post(reverse('password_change'), {
            'old_password': 'oldpassword123',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456'
        })
        self.assertEqual(response.status_code, 302)  # Редирект на профиль
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword456'))


class PasswordResetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')

    def test_password_reset(self):
        """Тест восстановления пароля"""
        response = self.client.post(reverse('password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)  # Редирект на `password_reset_done`
        # Проверяем, что отправлено письмо (Django Test Email Backend)
        self.assertEqual(len(response.wsgi_request._messages._queued_messages), 1)
