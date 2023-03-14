from django.views.generic import ListView, DeleteView

from apps.blog.models import Posts, Categories
from common.views import TitleMixin

class BlogView(TitleMixin, ListView):
    model = Posts
    template_name = 'blog/blog.html'
    title = 'Блог'
    category = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = Categories.objects.get(slug=self.kwargs['slug'])
            return queryset.filter(category_id=self.category.id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context["title"] = self.category.title
            
        return context
    


class BlogDetailView(TitleMixin, DeleteView):
    model = Posts
    template_name = 'blog/post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'{self.object.title} {self.object.id}'
        
        return context
    
    