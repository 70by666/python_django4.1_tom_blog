import datetime

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import ValidationError

from apps.users.models import User


class UserUpdateForm(UserChangeForm):
    """
    Форма обновления модели User
    """    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
            })

    def clean_birth_day(self):
        data = self.cleaned_data['birth_day']

        if data > datetime.date.today():
            raise ValidationError('Вы не могли родиться в будущем')

        if data < datetime.date.today() - datetime.timedelta(weeks=8000):
            raise ValidationError('Вам больше 150 лет?')
        
        return data
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 
                  'slug', 'birth_day', 'bio', 'image')
