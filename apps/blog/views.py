from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from apps.blog.forms import CommentCreateForm, EditPostForm, NewPostForm
from apps.blog.models import Categories, Comments, Posts
from common.mixins import (EditDeletePostRequiredMixin, IpMixin,
                           PostsTitleMixin, TitleMixin)


class BlogView(IpMixin, ListView):
    """
    Контроллер блога, отображение всех постов
    """
    model = Posts
    template_name = 'blog/blog.html'
    paginate_by = 6
    
    def get_queryset(self):
        """
        Сортировка по категориям и кэширование
        """
        queryset = cache.get('queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('queryset', queryset, 60)
            
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.paginate_by = None
            self.category = Categories.objects.get(slug=category_slug)
            sub_categories = self.category.get_descendants(include_self=True)
            return queryset.filter(category_id__in=sub_categories)
        
        return queryset
        
    def get_context_data(self, **kwargs):
        """
        Заголовок страницы в зависимости от категории
        """
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context['title'] = self.category.title if category_slug else 'Блог'
        
        return context
    

class BlogDetailView(IpMixin, LoginRequiredMixin, PostsTitleMixin, DetailView):
    """
    Контроллер отдельного поста
    """
    model = Posts
    template_name = 'blog/post.html'
    queryset = model.objects.detail()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreateForm
        
        return context


class AddlikeView(IpMixin, LoginRequiredMixin, View):
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


class CreateBlogPost(IpMixin, SuccessMessageMixin, LoginRequiredMixin, 
                     TitleMixin, CreateView):
    """
    Контроллер чтобы написать новую статью
    """
    title = 'Добавить статью'
    template_name = 'blog/new.html'
    form_class = NewPostForm
    model = Posts
    success_message = 'Статья добавлена'
    
    def get_success_url(self):
        return reverse_lazy('blog:index')
    
    def form_valid(self, form):
        """
        Запись в модель автора статьи при ее создании
        """
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Проверка на редактора
        """
        if not request.user.is_redactor:
            messages.info(request, 'Вы не редактор')
            return redirect('blog:index')
        
        return super().dispatch(request, *args, **kwargs)
    

class EditPostView(IpMixin, EditDeletePostRequiredMixin, SuccessMessageMixin, 
                   LoginRequiredMixin, PostsTitleMixin, UpdateView):
    """
    Контроллер для редактирования постов
    """
    model = Posts
    form_class = EditPostForm
    success_message = 'Статья изменена'
    template_name = 'blog/edit.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', args=(self.object.slug,))

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        
        return super().form_valid(form)
    

class DeletePostView(IpMixin, EditDeletePostRequiredMixin, SuccessMessageMixin, 
                     LoginRequiredMixin, PostsTitleMixin, DeleteView):
    """
    Контроллер для удаления постов
    """
    model = Posts
    success_message = 'Статья удалена'
    template_name = 'blog/delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:index')


class CommentCreateView(SuccessMessageMixin, IpMixin, 
                        LoginRequiredMixin, CreateView):
    """
    Контроллер для написания нового комментария под постом
    """
    model = Comments
    form_class = CommentCreateForm
    success_message = 'Комментарий добавлен'
    
    def get_success_url(self):
        return reverse_lazy('blog:post', args=(self.kwargs['slug'],))

    def form_valid(self, form):
        post = Posts.objects.get(slug=self.kwargs['slug'])
        form.instance.post = post
        form.instance.author = self.request.user
        if not self.kwargs['parent'] == int(0):
            print(self.kwargs['parent'])
            parent = Comments.objects.get(id=self.kwargs['parent'])
            form.instance.parent = parent
            
        form.save()
        
        return super().form_valid(form)


class PostsSearchResultView(ListView):
    """
    Контроллер поиска постов
    """
    model = Posts
    allow_empty = True
    template_name = 'blog/blog.html'
    
    def get_queryset(self):
        query = self.request.GET.get('do')
        search_vector = (
            SearchVector('full_description', weight='B') +
            SearchVector('title', weight='A')
        )
        search_query = SearchQuery(query)
        
        return (
            self.model.objects
            .annotate(rank=SearchRank(search_vector, search_query))
            .filter(rank__gte=0.3)
            .order_by('-rank')
            .select_related('author', 'category')
            .prefetch_related('likes', 'comments', 'comments__author')
            .filter(status=0)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("do")}'
        
        return context
