from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings


class SendMessageForm(forms.Form):
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, 
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, 
        label='ReCAPTCHA'
    )
    
    name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя',
            'autocomplete': 'off',
        }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Почта, чтобы получить наш ответ',
        'autocomplete': 'off',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Ваше сообщение',
        'autocomplete': 'off',
    }))
