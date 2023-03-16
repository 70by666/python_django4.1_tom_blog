from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

from common.utils import unique_slug


class User(AbstractUser):
    """
    Переопределение модели пользователей, чтобы почта была уникальной
    """
    email = models.EmailField(('email address'), unique=True)


class Profile(models.Model):
    """
    Модель для профиля пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def save(self, *args, **kwargs) -> None:
        """
        Генерация случайного slug
        """
        if not self.slug:
            self.slug = unique_slug(self, self.user.username)
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    @property
    def get_avatar(self):
        if self.image:
            return self.image.url
        
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()
