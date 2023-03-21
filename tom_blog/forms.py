from django import forms


class SendMessageForm(forms.Form):
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
