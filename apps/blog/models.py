from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class BlogPosts(models.Model):
    """
    Модель постов для блога
    """    

    PUBLISHED = 0
    DRAFT = 1
    STATUSES = (
        ('PUBLISHED', 'Черновик'),
        ('DRAFT', 'Опубликовано'),
    ) 
    
    title = models.CharField(verbose_name='Заголовок', max_length=128)
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=128, 
        blank=True, 
        unique=True,
    )
    short_descrtiprion = models.CharField(
        verbose_name='Короткое описание', 
        max_length=512,
    )
    full_description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(
        verbose_name='Превью',
        blank=True,
        upload_to='post_images',
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
    
    class Meta:
        ordering = ('-fixed', '-time_create')
        indexes = (models.Index(fields=('-fixed', '-time_crate', 'status')),)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.title
