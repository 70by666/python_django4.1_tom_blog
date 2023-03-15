from django.views.generic import ListView, TemplateView

from apps.blog.models import Posts
from common.views import TitleMixin


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
