from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.users.models import Ip, User


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
    и изменении пароля
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.request.user.id} - {self.request.user.username}'
        
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
    Миксин для создания и обновления профиля, установка placeholder
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
    """
    Миксин для заголовка страницы при просмотре поста или 
    редактировании/удалении поста 
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.id}-{self.object.title}'
        
        return context


class EditDeletePostRequiredMixin(AccessMixin):
    """
    Миксин для проверки порльзователя на то, является ли он 
    стаффом(администрастором) или автором статьи, чтобы удалить ее или 
    отредактировать
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
    
        messages.info(
            request, 
            'Вы не редактор/автор статьи!'
        )
        
        return redirect('blog:index')


class ObjectSuccessProfileMixin:
    """
    Миксин для редактирования профиля и изменения пароля, 
    возвращает текущего пользователя и выполняет метод для перенаправления 
    после формы
    """
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.slug,))


class IpLog:
    def get(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        print('###', request.user.is_authenticated)
        
        if not Ip.objects.filter(ip=ip).exists():
            if request.user.is_authenticated:
                user = request.user
                Ip.objects.create(user=user, ip=ip)
            else:
                Ip.objects.create(ip=ip)
        
        return super().get(request, *args, **kwargs)
