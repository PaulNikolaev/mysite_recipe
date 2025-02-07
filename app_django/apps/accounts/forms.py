from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.utils import timezone


from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control mb-1", "placeholder": "Придумайте новый логин"}),
        label="Логин"
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", "placeholder": "Введите новый email"}),
        label="Электронная почта"
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control mb-1", "placeholder": "Введите имя"}),
        label="Имя"
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control mb-1", "placeholder": "Введите фамилию"}),
        label="Фамилия"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email

    def __init__(self, *args, **kwargs):
        """
        Добавляем классы и placeholders для всех полей
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"autocomplete": "off", "class": "form-control mb-1"})


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    slug = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control mb-1", "placeholder": "Введите слаг (псевдоним)"}),
        label="Слаг (псевдоним)"
    )
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", "placeholder": "Дата рождения (ГГГГ-ММ-ДД)"}),
        label="Дата рождения (ГГГГ-ММ-ДД)"
    )
    bio = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 5, "class": "form-control mb-1", "placeholder": "Напишите что-то о себе"}),
        label="О себе"
    )
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control mb-1"}),
        label="Аватар"
    )

    class Meta:
        model = Profile
        fields = ('slug', 'birth_date', 'bio', 'avatar')

    def clean_birth_date(self):
        """
        Валидация даты рождения (например, не должно быть будущих дат)
        """
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError('Дата рождения не может быть в будущем')
        return birth_date

    def __init__(self, *args, **kwargs):
        """
        Обновляем виджеты и добавляем placeholder для всех полей
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"autocomplete": "off", "class": "form-control mb-1"})


class UserRegisterForm(UserCreationForm):
    """
    Переопределенная форма регистрации пользователей
    """

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "Придумайте свой логин"})
        self.fields['email'].widget.attrs.update({"placeholder": "Введите свой email"})
        self.fields['first_name'].widget.attrs.update({"placeholder": "Ваше имя"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Ваша фамилия"})
        self.fields['password1'].widget.attrs.update({"placeholder": "Придумайте свой пароль"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Повторите придуманный пароль"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы авторизации
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
        self.fields['username'].label = 'Логин'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class CustomPasswordResetForm(PasswordResetForm):
    """
    Кастомная форма сброса пароля с проверкой наличия email в базе данных.
    """
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден.")
        return email