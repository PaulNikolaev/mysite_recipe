from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.forms import (UserUpdateForm,
                                 ProfileUpdateForm,
                                 UserRegisterForm,
                                 UserLoginForm,
                                 CustomPasswordResetForm)
from apps.accounts.models import Profile
from datetime import date


class TestForms(TestCase):

    def setUp(self):
        """Очистка базы и создание тестового пользователя"""
        User.objects.all().delete()
        Profile.objects.all().delete()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            slug='testuser123',
            birth_date=date(2000, 1, 1),
            bio='Test bio',
        )

    @classmethod
    def tearDownClass(cls):
        Profile.objects.all().delete()
        User.objects.all().delete()
        super().tearDownClass()

    def test_user_update_form_valid(self):
        """Тестируем, что форма UserUpdateForm корректно обновляет данные пользователя"""
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_user_update_form_invalid_email(self):
        """Тестируем, что форма UserUpdateForm валидирует уникальность email"""
        User.objects.create_user(
            username='otheruser',
            password='password123',
            email='other@example.com',
            first_name='Other',
            last_name='User'
        )
        form_data = {
            'username': 'updateduser',
            'email': 'other@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Email адрес должен быть уникальным'])

    def test_profile_update_form_valid(self):
        """Тестируем, что форма ProfileUpdateForm корректно обновляет профиль"""
        form_data = {
            'slug': 'updatedslug',
            'birth_date': '1995-05-15',
            'bio': 'Updated bio',
            'avatar': None  # Пустой аватар
        }
        form = ProfileUpdateForm(instance=self.profile, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.slug, 'updatedslug')
        self.assertEqual(self.profile.birth_date, date(1995, 5, 15))
        self.assertEqual(self.profile.bio, 'Updated bio')

    def test_profile_update_form_invalid_birth_date(self):
        """Тестируем, что форма ProfileUpdateForm валидирует дату рождения"""
        form_data = {
            'slug': 'updatedslug',
            'birth_date': str(date.today().year + 1) + '-01-01',  # Невозможная будущая дата
            'bio': 'Updated bio',
            'avatar': None
        }
        form = ProfileUpdateForm(instance=self.profile, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['birth_date'], ['Дата рождения не может быть в будущем'])

    def test_user_register_form_valid(self):
        """Тестируем, что форма UserRegisterForm корректно регистрирует пользователя"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_user_register_form_invalid_email(self):
        """Тестируем, что форма UserRegisterForm валидирует уникальность email"""
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',  # Используем уже существующий email
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Такой email уже используется в системе'])

    def test_user_login_form_valid(self):
        """Тестируем, что форма UserLoginForm корректно проходит аутентификацию"""
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_login_form_invalid(self):
        """Тестируем, что форма UserLoginForm не проходит с неправильными данными"""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Неверный логин или пароль.'])

    def test_password_reset_form_valid(self):
        """Тестируем, что форма сброса пароля корректно валидирует email"""
        form_data = {'email': 'test@example.com'}
        form = CustomPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_reset_form_invalid_email(self):
        """Тестируем, что форма сброса пароля валидирует отсутствие email в базе данных"""
        form_data = {'email': 'nonexistent@example.com'}
        form = CustomPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Пользователь с таким email не найден.'])
