import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now

from apps.users.models import Ip


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


class IpMixin:
    """
    Миксин для заполнения модели Ip
    """
    def get(self, request, *args, **kwargs):
        ip = self.get_ip(request)
        
        user = request.META.get('USER')
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(user=user, ip=ip)
        else:
            ip = Ip.objects.get(ip=ip)
            if ip.is_banned:
                context = {
                    'title': '403 Ошибка доступа.', 
                    'message': 'бан',
                }
                return render(request, 'error.html', context)
            
            ip.updated = now
            ip.save()
        
        return super().get(request, *args, **kwargs)
    
    def ban(self, request, data=None):
        """
        Забанить
        """
        ip = self.get_ip(request)
        self.send_telegram_message(ip=ip)
        ip = Ip.objects.get(ip=ip)
        ip.is_banned = True
        ip.save()
            
    def send_telegram_message(self, message=None, ip=None):
        """
        Отправка сообщения в телеграме
        """
        if not message:
            message = f'Забанен {ip}'
            
        for i in settings.CHAT_IDS.split():
            url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
                settings.BOT_TOKEN, 
                i,
                message,
            )
            requests.post(url)

    def get_ip(self, request):
        """
        Получить IP
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        return ip


class NoAuthRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Перенаправление авторизованных пользователей
        """
        if request.user.is_authenticated:
            return redirect(reverse_lazy(
                'users:profile', 
                args=(self.request.user.slug,)
            ))
            
        return super().dispatch(request, *args, **kwargs)
