from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

from common.utils import unique_slug


class User(AbstractUser):
    """
    Переопределение модели пользователей
    """
    email = models.EmailField(('email address'), unique=True)
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=150, 
        unique=True, 
        blank=True
    )
    image = models.ImageField(
        verbose_name='Аватар',
        blank=True,
        upload_to='users_images/%y/%m/%d',
        validators=[FileExtensionValidator(allowed_extensions=(
            'png', 'jpg', 'jpeg', 'gif', 'webp'
        ))],
    )
    bio = models.TextField(verbose_name='Информации о себе', blank=True)
    birth_day = models.DateField(
        blank=True, 
        null=True, 
        verbose_name='Дата рождения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def save(self, *args, **kwargs) -> None:
        """
        Автоматическая генерация slug и 
        при необходимости генерация случайного slug
        """
        if not self.slug:
            self.slug = unique_slug(self, self.username)
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def get_avatar(self):
        if self.image:
            return self.image.url
        
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'
