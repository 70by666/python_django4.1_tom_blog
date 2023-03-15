from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    """
    Переопределение модели пользователей
    """
    image = models.ImageField(
        verbose_name='Аватарка',
        blank=True,
        null=True,
        upload_to='users_images/%y/%m/%d',
        validators=[FileExtensionValidator(allowed_extensions=(
            'png', 'jpg', 'jpeg', 'gif', 'webp'
        ))]
    )
    email = models.EmailField(('email address'), unique=True)

    def save(self, *args, **kwargs) -> None:
        """
        Добавляю username к названию изображения
        """
        self.image.name = f'{self.username}_{self.image}'
        
        return super().save(*args, **kwargs)
