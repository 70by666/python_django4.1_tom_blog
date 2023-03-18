from django import forms


class SendMessageForm(forms.Form):
    name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={
            'class': 'form_control',
            'placeholder': 'Введите имя',
        }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form_control',
        'placeholder': 'Почта, чтобы получить наш ответ',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form_control',
        'placeholder': 'Ваше сообщение',
    }))
