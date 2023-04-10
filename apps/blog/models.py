from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from apps.users.models import Ip, User
from services.utils import unique_slug


class Posts(models.Model):
    """
    Модель постов для блога
    """    
    class PostsManager(models.Manager):
        def all(self):
            """
            Переопределил метод all чтобы получать посты только со статусом
            "опубликовано" и оптимизация запросов
            """
            return (
                self.get_queryset()
                .select_related('author', 'category')
                .prefetch_related('likes', 'comments', 'comments__author', 'views')
                .filter(status=0)
            )
        
        def detail(self):
            """
            Оптимизация запросов
            """
            return (
                self.get_queryset()
                .select_related('author', 'category')
                .prefetch_related('comments', 'comments__author', 'likes', 'views')
                .filter(status=0)
            )
        
    PUBLISHED = 0
    DRAFT = 1
    STATUSES = (
        (PUBLISHED, 'Опубликовано'),
        (DRAFT, 'Черновик'),
    ) 
    
    title = models.CharField(verbose_name='Заголовок', max_length=32)
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=32, 
        blank=True,
        unique=True
    )
    short_description = models.CharField(
        verbose_name='Короткое описание', 
        max_length=128,
        blank=True,
    )
    full_description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(
        verbose_name='Превью',
        upload_to='post_images/%y/%m/%d',
        validators=[FileExtensionValidator(allowed_extensions=(
            'png', 'jpg', 'jpeg', 'gif', 'webp'
        ))]
    )
    status = models.PositiveSmallIntegerField(
        default=PUBLISHED, 
        choices=STATUSES,
        verbose_name='Статус поста'
    )
    created = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Время добавления',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления',
    )
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.PROTECT,
        related_name='author_posts',
    )
    updater = models.ForeignKey(
        to=User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Обновил',
        related_name='updated_posts',
    )
    fixed = models.BooleanField(verbose_name='Закреплено', default=False)
    category = TreeForeignKey(
        'Categories', 
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория'
    )
    likes = models.ManyToManyField(
        to=User, 
        blank=True, 
        default=0, 
        related_name='likes'
    )
    views = models.ManyToManyField(
        to=Ip, 
        blank=True, 
        default=0, 
        related_name='views'
    )
    
    objects = PostsManager()
    
    class Meta:
        ordering = ('-created', )
        indexes = (models.Index(fields=('-fixed', '-created', 'status')),)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Автоматическая генерация slug и 
        при необходимости генерация случайного slug
        """
        if not self.slug:
            self.slug = unique_slug(self, self.title)
                
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})
    
    
class Categories(MPTTModel):
    """
    Модель для категорий с вложенностью
    """
    title = models.CharField(
        max_length=32, 
        verbose_name='Название',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=32, 
        blank=True, 
        unique=True,
    )
    description = models.CharField(
        max_length=64,
        verbose_name='Описание',
        blank=True,
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Родительская категория'
    )
    
    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)
   
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.title


class Comments(MPTTModel):
    """
    Модель для древовидных комментариев
    """
    post = models.ForeignKey(
        Posts, 
        on_delete=models.CASCADE, 
        verbose_name='Пост', 
        related_name='comments',
    )
    author = models.ForeignKey(
        User, 
        verbose_name='Автор комментария', 
        on_delete=models.CASCADE, 
        related_name='comments_author',
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        verbose_name='Время добавления', 
        auto_now_add=True
    )
    parent = TreeForeignKey(
        'self', 
        verbose_name='Родительский комментарий', 
        null=True, 
        blank=True, 
        related_name='children', 
        on_delete=models.CASCADE
    )
    
    class MTTMeta:
        order_insertion_by = ('-created',)

    class Meta:
        indexes = [models.Index(fields=['-created', 'parent'])]
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.text}'
