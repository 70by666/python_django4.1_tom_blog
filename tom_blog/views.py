from http import HTTPStatus

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from apps.blog.models import Posts
from services.ban import ban
from services.mixins import TitleMixin
from tom_blog.forms import SendMessageForm
from tom_blog.tasks import send_telegram_message_task


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
    
    def form_valid(self, form):
        """
        Проверка сообщения, если оно не подходит ip банится, если подходит то 
        отправляется через метод
        """
        data = form.data
        message = data["message"]
        banword = ('mutk.pro', 'esgeni.tk')
        for i in banword:
            if i in message:
                ban(request=self.request)
                return redirect('index')

        message = f'{data["name"]}\n{data["email"]}\n{message}'
        send_telegram_message_task.delay(message=message)
            
        return super().form_valid(form)


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
