from django.db import models
from django.utils.timezone import now


class TgAuth(models.Model):
    """
    Модель для подтверждения почты
    """
    code = models.UUIDField(unique=True)
    tg_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    is_valid = models.BooleanField(default=True)

    def is_expired(self):
        """
        Проверка на срок действия письма
        """
        return True if now() <= self.expiration else False 
