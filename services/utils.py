from uuid import uuid4

import requests
from django.conf import settings
from pytils.translit import slugify


def unique_slug(title, instance=None, model=None):
    """
    Функция для генерации случайного slug
    """
    if model:
        model = model
    else:
        model = instance.__class__
        
    slug = slugify(title)
    if not slug:
        slug = f'{uuid4().hex[:8]}'

    while model.objects.filter(slug=slug).exists():
        slug = f'{slug}-{uuid4().hex[:8]}'
        
    return slug


def send_telegram_message(message=None, ip=None):
    """
    Отправка сообщения в телеграме
    """
    if not message:
        message = f'Забанен {ip}'
        
    for i in settings.CHAT_IDS.split():
        url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
            settings.BOT_TOKEN, 
            i,
            message,
        )
        requests.post(url)


def get_ip(request):
    """
    Получить IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    return ip
