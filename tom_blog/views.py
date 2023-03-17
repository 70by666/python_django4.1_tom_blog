from http import HTTPStatus

from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from apps.blog.models import Posts
from common.mixins import TitleMixin


class IndexView(TitleMixin, ListView):
    model = Posts
    template_name = 'index.html'
    title = 'Домашняя страница' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = super().get_queryset()[:3]
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        return queryset.filter(fixed=True)
    
    
class ContactView(TitleMixin, TemplateView):
    template_name = 'contact.html'
    title = 'Обратная связь'


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
