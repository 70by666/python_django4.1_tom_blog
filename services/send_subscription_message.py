from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from apps.users.models import Subscription


def send_subscription_message(title, short_description, slug):
    subscription = Subscription.objects.all()
    for i in subscription:
        link = settings.DOMAIN_NAME + reverse('blog:post', args=(slug,))
        subject = f'На сайте новая статья {title}'
        message = f'Короткое описание: {short_description}\nСсылка на новую статью {link}'
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER, 
            [i.user.email], 
            fail_silently=False
        )
