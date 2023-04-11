from celery import shared_task

from services.utils import send_telegram_message
from services.send_subscription_message import send_subscription_message


@shared_task
def send_telegram_message_task(message=None, ip=None):
    """
    Отложенная задача для отправки сообщения в телеграм через celery
    """
    return send_telegram_message(message=message, ip=ip)


@shared_task
def send_subscription_message_task(title, short_description, slug):
    """
    Отложенная задача для отправки уведомления о новом посте
    """
    return send_subscription_message(title, short_description, slug)
