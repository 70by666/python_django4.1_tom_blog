from django.shortcuts import redirect
from django.views.generic import DeleteView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.blog.models import Categories, Posts
from common.views import TitleMixin


class BlogView(TitleMixin, ListView):
    model = Posts
    template_name = 'blog/blog.html'
    title = 'Блог'
    category = None
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = Categories.objects.get(slug=self.kwargs['slug'])
            return queryset.filter(category_id=self.category.id)
        
        return queryset.filter(status=0)
    
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
        context['title'] = f'{self.object.title} - ID {self.object.id}'
        
        return context


class AddlikeView(LoginRequiredMixin, View):
    def get(self, request, slug, *args, **kwargs):
        post = Posts.objects.get(slug=slug)
        for like in post.likes.all():
            if like == request.user:
                post.likes.remove(request.user)
                return redirect(request.META['HTTP_REFERER'])
            
        post.likes.add(request.user)
        
        return redirect(request.META['HTTP_REFERER'])
