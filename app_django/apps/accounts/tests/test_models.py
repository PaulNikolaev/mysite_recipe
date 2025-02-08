from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.utils import timezone
from apps.accounts.models import Profile
from datetime import date


class ProfileModelTest(TestCase):

    def setUp(self):
        """Создание тестового пользователя и профиля"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            slug='testuser-slug',
            birth_date=date(2000, 1, 1),
            bio='This is a test bio'
        )

    def tearDown(self):
        """Очистка базы данных после теста"""
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_profile_creation(self):
        """Тестируем, что профиль создается корректно"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.slug, 'testuser-slug')
        self.assertEqual(self.profile.birth_date, date(2000, 1, 1))
        self.assertEqual(self.profile.bio, 'This is a test bio')

    def test_auto_slug_generation(self):
        """Тестируем, что слаг генерируется автоматически, если не указан"""
        profile = Profile.objects.create(user=self.user)
        self.assertNotEqual(profile.slug, '')  # Проверяем, что слаг не пустой
        self.assertTrue(profile.slug.startswith('testuser'))  # Должен содержать имя пользователя

    def test_get_absolute_url(self):
        """Тестируем метод get_absolute_url"""
        expected_url = f'/accounts/profile/{self.profile.slug}/'
        self.assertEqual(self.profile.get_absolute_url(), expected_url)

    def test_is_online_true(self):
        """Тестируем, что is_online работает корректно (пользователь онлайн)"""
        cache.set(f'last-seen-{self.user.id}', timezone.now(), timeout=300)
        self.assertTrue(self.profile.is_online)

    def test_is_online_false(self):
        """Тестируем, что is_online работает корректно (пользователь офлайн)"""
        cache.set(f'last-seen-{self.user.id}', timezone.now() - timezone.timedelta(minutes=10), timeout=300)
        self.assertFalse(self.profile.is_online)

    def test_avatar_upload(self):
        """Тестируем загрузку аватара"""
        avatar = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00',
            content_type='image/jpeg'
        )
        self.profile.avatar = avatar
        self.profile.save()
        self.assertTrue(self.profile.avatar.name.startswith('images/avatars/'))

    def test_birth_date_validation(self):
        """Тестируем валидацию даты рождения (не может быть в будущем)"""
        self.profile.birth_date = date.today() + timezone.timedelta(days=1)
        with self.assertRaises(Exception):
            self.profile.save()