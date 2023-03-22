import datetime

from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.forms import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

from apps.users.models import User
from common.mixins import StyleFormMixin, PlaceholderCreateUpdateForm


class UserUpdateForm(PlaceholderCreateUpdateForm, StyleFormMixin, UserChangeForm):
    """
    Форма обновления модели User
    """    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].widget.attrs.update(
            {"placeholder": 'Введите ссылку на ваш профиль'}
        )
        self.fields['birth_day'].widget.attrs.update(
            {"placeholder": 'Введите дату рождения'}
        )
        self.fields['bio'].widget.attrs.update(
            {"placeholder": 'Введите информацию о себе'}
        )
    
    def clean_birth_day(self):
        data = self.cleaned_data['birth_day']

        if data:
            if data > datetime.date.today():
                raise ValidationError('Вы не могли родиться в будущем')

            if data < datetime.date.today() - datetime.timedelta(weeks=8000):
                raise ValidationError('Вам больше 150 лет?')
        
        return data
    
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 
            'slug', 'birth_day', 'bio', 'image',
        )


class LoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для авторизации
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {"placeholder": 'Введите имя пользователя'}
        )
        self.fields['password'].widget.attrs.update(
            {"placeholder": 'Введите пароль'}
        )
    
    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(PlaceholderCreateUpdateForm, StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {"placeholder": 'Придумайте пароль'}
        )
        self.fields['password2'].widget.attrs.update(
            {"placeholder": 'Повторите пароль'}
        )
        
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 
            'last_name', 'password1', 'password2',
        )


class ChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    """
    Форма для смены пароля, только чтобы применить стили
    """
