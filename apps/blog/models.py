from uuid import uuid4

from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse

from mptt.models import TreeForeignKey, MPTTModel
from pytils.translit import slugify

User = get_user_model()


class Posts(models.Model):
    """
    Модель постов для блога
    """    

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
        max_length=64,
        blank=True,
    )
    full_description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(
        verbose_name='Превью',
        blank=True,
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
    fixed = models.BooleanField(
        verbose_name='Закреплено',
        default=False
    )
    category = TreeForeignKey(
        'Categories', 
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория'
    )
    
    class Meta:
        ordering = ('-fixed', '-created')
        indexes = (models.Index(fields=('-fixed', '-created', 'status')),)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Генерация случайноuj slug, если уже есть статья с нужным названием
        """
        
        if not self.slug:
            self.slug = slugify(self.title)
            while Posts.objects.filter(slug=self.slug).exists():
                self.slug = f'{self.slug}-{uuid4().hex[:8]}'
                
        return super().save(*args, **kwargs)
    
    
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
