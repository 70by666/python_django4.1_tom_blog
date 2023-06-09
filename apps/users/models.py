from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

from services.utils import unique_slug


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
    is_redactor = models.BooleanField(
        verbose_name='Статус редактор', 
        default=False
    )
    tg_id = models.IntegerField(
        blank=True, 
        null=True, 
        verbose_name='ИД пользователя в телеграме'
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
            self.slug = unique_slug(instance=self, title=self.username)
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def get_avatar(self):
        """
        Получить аватар
        """
        if self.image:
            return self.image.url
        
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'

    def is_online(self):
        last_seen = cache.get(f'last-seen-{self.id}')
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        
        return False


class EmailVerification(models.Model):
    """
    Модель для подтверждения почты
    """
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f'EmailVerification object for {self.user.username}'

    def send_verification_email(self, new_email=None):
        """
        Отправка письма
        """
        if not new_email:
            new_email = self.user.email
        
        link = reverse('users:email', args=(new_email, self.code))
        verificationlink = settings.DOMAIN_NAME + link
        subject = f'Подтверждение почты для {self.user.username}'
        message = f'Для подтверждения почты {new_email} перейдите по ссылке {verificationlink}'
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER, 
            [new_email], 
            fail_silently=False
        )

    def is_expired(self):
        """
        Проверка на срок действия письма
        """
        return True if now() <= self.expiration else False 


class Ip(models.Model):
    """
    Модель для лога IP
    """
    user = models.CharField(max_length=150, default='Anonymous')
    ip = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True
    )
    is_banned = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Пользователь {self.user} | {self.ip}'


class ProfileComments(models.Model):    
    """
    Модель комментариев под профилем
    """    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь', 
        related_name='comments_profile',
    )
    author = models.ForeignKey(
        User, 
        verbose_name='Автор комментария', 
        on_delete=models.CASCADE, 
        related_name='comments_author_profile',
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        verbose_name='Время добавления', 
        auto_now_add=True
    )

    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.text}'


class Subscription(models.Model):
    """
    Модель для подписчиков на рассылку
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
