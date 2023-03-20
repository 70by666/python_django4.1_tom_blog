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


# class SendMessageForm(InitFormMixin, forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].widget.attrs.update({
#             'class': 'form_control',
#             "placeholder": 'Введите имя',
#         })
#         self.fields['email'].widget.attrs.update({
#             'class': 'form_control',
#             "placeholder": 'Почта, чтобы получить наш ответ'
#         })
#         self.fields['message'].widget.attrs.update({
#             'class': 'form_control',
#             "placeholder": 'Ваше сообщение'
#         })
    
#     class Meta:
#         fields = ('name', 'email', 'message')