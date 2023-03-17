from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.blog.models import Categories, Posts
from common.mixins import TitleMixin


class BlogView(ListView):
    """
    Представвление блога
    """
    model = Posts
    template_name = 'blog/blog.html'
    category = None
    paginate_by = 6
    
    def get_queryset(self):
        """
        Сортировка по категориям
        """
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = Categories.objects.get(slug=category_slug)
            return queryset.filter(category_id=self.category.id)
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context["title"] = self.category.title if category_slug else 'Блог'
        
        return context
    

class BlogDetailView(TitleMixin, DetailView):
    """
    Представление отдельного поста
    """
    model = Posts
    template_name = 'blog/post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.id}-{self.object.title}'
        
        return context


class AddlikeView(LoginRequiredMixin, View):
    """
    Поставить лайк
    """
    def get(self, request, slug, *args, **kwargs):
        post = Posts.objects.get(slug=slug)
        for like in post.likes.all():
            if like == request.user:
                post.likes.remove(request.user)
                return redirect(request.META['HTTP_REFERER'])
            
        post.likes.add(request.user)
        
        return redirect(request.META['HTTP_REFERER'])
