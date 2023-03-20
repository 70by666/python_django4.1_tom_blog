from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View, CreateView
from django.contrib.messages.views import SuccessMessageMixin

from apps.blog.forms import NewPostForm
from apps.blog.models import Categories, Posts
from common.mixins import TitleMixin


class BlogView(ListView):
    """
    Контрллер блога, отображение всех постов
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
    Контроллер отдельного поста
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


class CreateBlogPost(SuccessMessageMixin, LoginRequiredMixin, TitleMixin, CreateView):
    title = 'Добавить статью'
    template_name = 'blog/new.html'
    form_class = NewPostForm
    model = Posts
    success_message = 'Статья добавлена'
    
    def get_success_url(self):
        return reverse_lazy('blog:index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
