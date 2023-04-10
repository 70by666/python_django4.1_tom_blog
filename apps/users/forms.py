import datetime

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserChangeForm, UserCreationForm)
from django.forms import ValidationError

from apps.users.models import ProfileComments, User
from apps.users.tasks import send_email_verify
from common.mixins import PlaceholderCreateUpdateForm, StyleFormMixin


class UserUpdateForm(PlaceholderCreateUpdateForm, StyleFormMixin, UserChangeForm):
    """
    Форма обновления модели User
    """    
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )
    
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
    
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 
            'slug', 'birth_day', 'bio', 'image',
        )
    
    def clean_birth_day(self):
        """
        Проверка даты рождения
        """
        data = self.cleaned_data['birth_day']

        if data:
            if data > datetime.date.today():
                raise ValidationError('Вы не могли родиться в будущем')

            if data < datetime.date.today() - datetime.timedelta(weeks=8000):
                raise ValidationError('Вам больше 150 лет?')
        
        return data


class LoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для авторизации
    """
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )
    
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
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )
        
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

    def save(self, commit=True):
        """
        Отправка письма после регистрации
        """
        user = super().save(commit)
        send_email_verify.delay(user.id)
        
        return user


class ChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    """
    Форма для смены пароля
    """
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )


class ResetPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос восстановления пароля
    """
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )


class SetPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Форма восстановления пароля
    """
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )


class ProfileCommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев под профилем
    """
    text = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={
            'cols': 30, 'rows': 3, 'placeholder': 'Комментарий', 
            'class': 'form-control shadow-none textarea bg-form',
        }),
    )

    class Meta:
        model = ProfileComments
        fields = ('text',)
