from django.views.generic import TemplateView, ListView

from common.views import TitleMixin
from apps.blog.models import Posts


class IndexView(TitleMixin, ListView):
    model = Posts
    template_name = 'index.html'
    title = 'Домашняя страница' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = super().get_queryset()
        context['filter'] = queryset.order_by('created')[:3]
        
        return context
    
    
class ContactView(TitleMixin, TemplateView):
    template_name = 'contact.html'
    title = 'Обратная связь'
