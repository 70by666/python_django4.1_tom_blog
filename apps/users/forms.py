import datetime

from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UserCreationForm
from django.forms import ValidationError

from apps.users.models import User
from common.mixins import InitFormMixin


class UserUpdateForm(InitFormMixin, UserChangeForm):
    """
    Форма обновления модели User
    """    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите фамилию',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес электронной почты',
    }))
    slug = forms.SlugField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите ссылку на ваш профиль',
    }))
    birth_day = forms.DateField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Введите дату рождения',
        'type': 'date',
    }))    
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Введите информацию о себе',
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput())
    
    def clean_birth_day(self):
        data = self.cleaned_data['birth_day']

        if data > datetime.date.today():
            raise ValidationError('Вы не могли родиться в будущем')

        if data < datetime.date.today() - datetime.timedelta(weeks=8000):
            raise ValidationError('Вам больше 150 лет?')
        
        return data
    
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 
            'slug', 'birth_day', 'bio', 'image'
        )


class LoginForm(InitFormMixin, AuthenticationForm):
    """
    Форма для авторизации
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
    }))
    
    class Meta:
        model = User
        fields = ('username', 'password')


# нужно проерить mixin на одинаковые поля
class RegisterForm(InitFormMixin, UserCreationForm):
    """
    Форма для регистрации
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Придумайте имя пользователя',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес электронной почты',
    }))    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите фамилию',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Придумайте пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Для подтверждения пароля введите его еще раз',
    }))
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 
            'last_name', 'password1', 'password2',
        )
