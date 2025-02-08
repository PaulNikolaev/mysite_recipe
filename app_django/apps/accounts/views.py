import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, CreateView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordResetView,
                                       PasswordResetConfirmView)

from .models import Profile
from .forms import (UserUpdateForm,
                    ProfileUpdateForm,
                    UserRegisterForm,
                    UserLoginForm,
                    CustomPasswordResetForm)
from ..recipe.models import Category

logger = logging.getLogger(__name__)


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя: {self.object.user.username}'
        context['categories'] = Category.objects.all()
        logger.info(f'Просмотр профиля пользователя: {self.object.user.username}')
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        context['categories'] = Category.objects.all()
        context['slug'] = self.object.slug
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
                logger.info(f'Профиль пользователя {self.request.user.username} успешно обновлен')
            else:
                logger.warning(f'Ошибка при обновлении профиля {self.request.user.username}')
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Новый пользователь зарегистрирован: {self.object.username}')
        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    next_page = 'home'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Пользователь вошел в систему: {self.request.user.username}')
        return response


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = 'home'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Изменение пароля
    """
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.request.user.profile.slug
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Пользователь {self.request.user.username} изменил пароль')
        return response

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """
    Восстановление пароля с проверкой email.
    """
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/accounts/password-reset/done/'
    success_message = 'Инструкции по восстановлению пароля отправлены на ваш email.'

    def get_context_data(self, **kwargs):
        """
        Добавляем данные в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Восстановление пароля'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Запрос на сброс пароля для email: {form.cleaned_data["email"]}')
        return response


class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Подтверждение сброса пароля
    """
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/reset/done/'
    success_message = 'Ваш пароль успешно изменен.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установка нового пароля'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Пользователь успешно сбросил пароль')
        return response
