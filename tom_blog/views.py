from http import HTTPStatus

from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from apps.blog.models import Posts
from common.views import TitleMixin, title_error


class IndexView(TitleMixin, ListView):
    model = Posts
    template_name = 'index.html'
    title = 'Домашняя страница' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = super().get_queryset()
        context['filter'] = queryset.order_by('created')[:3]
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        return queryset.all()[:3]
    
    
class ContactView(TitleMixin, TemplateView):
    template_name = 'contact.html'
    title = 'Обратная связь'


def error403(request, exception):
    context = title_error('Ошибка доступа: 403')
    status = HTTPStatus.FORBIDDEN
    
    return render(request, '403.html', context, status=status)


def error404(request, exception):
    context = title_error('Страница не найдена: 404')
    status = HTTPStatus.NOT_FOUND
    
    return render(request, '404.html', context, status=status)


def error500(request):
    context = title_error('Ошибка сервера: 500')
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    
    return render(request, '500.html', context, status=status)
