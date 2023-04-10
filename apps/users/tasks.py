import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from apps.users.models import EmailVerification, User


@shared_task
def send_verification_email_task(user_id, new_email=None):
    """
    Отложенная задача, отправка письма через celery, заполнение модели
    """
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    
    expiration = now() + timedelta(hours=24)
    record = EmailVerification.objects.create(code=uuid.uuid4(), 
                                                user=user, 
                                                expiration=expiration)
    record.send_verification_email(new_email)
