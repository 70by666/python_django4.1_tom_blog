from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from apps.blog.forms import EditPostForm, NewPostForm
from apps.blog.models import Categories, Posts
from common.mixins import PostsTitleMixin, TitleMixin, EditDeletePostRequiredMixin


class BlogView(ListView):
    """
    Контрллер блога, отображение всех постов
    """
    model = Posts
    template_name = 'blog/blog.html'
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
    

class BlogDetailView(PostsTitleMixin, DetailView):
    """
    Контроллер отдельного поста
    """
    model = Posts
    template_name = 'blog/post.html'


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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_redactor:
            messages.info(request, 'Вы не редактор')
            return redirect('blog:index')
        
        return super().dispatch(request, *args, **kwargs)
    

class EditPostView(EditDeletePostRequiredMixin, SuccessMessageMixin, 
                   LoginRequiredMixin, PostsTitleMixin, UpdateView):
    model = Posts
    form_class = EditPostForm
    success_message = 'Статья изменена'
    template_name = 'blog/edit.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', args=(self.object.slug,))


class DeletePostView(EditDeletePostRequiredMixin, SuccessMessageMixin, 
                     LoginRequiredMixin, PostsTitleMixin, DeleteView):
    model = Posts
    success_message = 'Статья удалена'
    template_name = 'blog/delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:index')
