from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class TitleMixin:
    """
    Миксин для заголовка страницы в представлениях
    """
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        
        return context


class ProfileTitleMixin:
    """
    Миксин для заголовка страницы в представлениях профиля и его редактирования
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.id} - {self.object.username}'
        
        return context


class StyleFormMixin:
    """
    Миксин для применения стилей к input в формах
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
            })


class PlaceholderCreateUpdateForm:
    """
    Миксин для создания и обновления профиля
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {"placeholder": 'Введите имя пользователя'}
        )
        self.fields['first_name'].widget.attrs.update(
            {"placeholder": 'Введите имя'}
        )
        self.fields['last_name'].widget.attrs.update(
            {"placeholder": 'Введите фамилию'}
        )
        self.fields["email"].widget.attrs.update(
            {"placeholder": 'Введите адрес электронной почты'}
        )


class PostsTitleMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.id}-{self.object.title}'
        
        return context


class EditDeletePostRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
    
        messages.info(
            request, 
            'Вы не редактор/автор статьи!'
        )
        
        return redirect('blog:index')
