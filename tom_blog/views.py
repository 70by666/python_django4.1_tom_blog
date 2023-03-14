from django.views.generic import TemplateView

from common.views import CommonContextMixin


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'index.html'
    title = 'Домашняя страница' 


class ContactView(CommonContextMixin, TemplateView):
    template_name = 'contact.html'
    title = 'Обратная связь'
