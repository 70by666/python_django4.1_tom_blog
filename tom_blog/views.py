from http import HTTPStatus

import requests
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from apps.blog.models import Posts
from common.mixins import TitleMixin
from tom_blog.forms import SendMessageForm


class IndexView(TitleMixin, ListView):
    """
    Контроллер основной страницы
    """
    model = Posts
    template_name = 'index.html'
    title = 'Домашняя страница' 
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        """
        Получение последних трех постов
        """
        context = super().get_context_data(**kwargs)
        context['last_posts'] = self.queryset[1:3]
        context['first'] = self.queryset[:3].first()
        
        return context
    
    def get_queryset(self):
        """
        Получение закрепленных постов
        """
        return self.queryset.filter(fixed=True)
    
    
class ContactView(SuccessMessageMixin, TitleMixin, FormView):
    """
    Контроллер формы обратной связи
    """
    template_name = 'contact.html'
    title = 'Обратная связь'
    form_class = SendMessageForm
    success_url = reverse_lazy('contact')
    success_message = 'Сообщение отправлено!'
    
    def post(self, request, *args, **kwargs):
        """
        Отправка сообщений на указанные ИД телеграм чатов
        Можно было бы прописать логику при методе save в моделе, но не хотел
        создать модель
        """
        form = self.get_form()
        if form.is_valid():
            data = form.data
            for i in settings.CHAT_IDS.split():
                url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
                    settings.BOT_TOKEN, 
                    i,
                    f'{data["name"]}\n{data["email"]}\n{data["message"]}',
                )
                requests.post(url)
        
        return super().post(self, request, *args, **kwargs)


def error403(request, exception):
    context = {
        'title': '403 Ошибка доступа.', 
        'message': 'Нет доступа к этой странице.',
    }
    status = HTTPStatus.FORBIDDEN
    
    return render(request, 'error.html', context, status=status)


def error404(request, exception):
    context = {
        'title': '404 Страница не найдена.', 
        'message': 'Страница не была найдена, или она никогда не существовала,'
                   ' или была удалена, или перемещена.',
    }
    status = HTTPStatus.NOT_FOUND
    
    return render(request, 'error.html', context, status=status)


def error500(request):
    context = {
        'title': '500 Ошибка сервера.', 
        'message': 'Внутренняя ошибка сервера, вернитесь на главную страницу, '
                   'отчет мы направим разработчику.',
    }
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    
    return render(request, 'error.html', context, status=status)
