from django.views.generic import ListView, DeleteView

from apps.blog.models import Posts
from common.views import TitleMixin

class BlogView(TitleMixin, ListView):
    model = Posts
    template_name = 'blog/blog.html'
    title = 'Блог'


class BlogDetailView(TitleMixin, DeleteView):
    model = Posts
    template_name = 'blog/post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'{self.object.title} {self.object.id}'
        
        return context
    
    