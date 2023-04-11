from celery import shared_task

from services.send_subscription_message import send_subscription_message


@shared_task
def send_subscription_message_task(title, short_description, slug):
    """
    Отложенная задача для отправки уведомления о новом посте
    """
    return send_subscription_message(title, short_description, slug)
