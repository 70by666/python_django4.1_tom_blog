from celery import shared_task

from services.utils import send_telegram_message


@shared_task
def send_telegram_message_task(message=None, ip=None):
    """
    Отложенная задача для отправки сообщения в телеграм через celery
    """
    return send_telegram_message(message=message, ip=ip)
