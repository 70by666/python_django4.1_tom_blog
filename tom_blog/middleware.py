from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from apps.users.models import Ip, User
from services.utils import get_ip


class ActiveUserMiddleware(MiddlewareMixin):
    """
    Обновления поля last_login у пользователей и статус онлайн/не в сети
    """
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_login = cache.get(cache_key)
            if not last_login:
                User.objects.filter(id=request.user.id).update(
                    last_login=timezone.now()
                )
                cache.set(cache_key, timezone.now(), 60)


class IpMiddleware(MiddlewareMixin):
    """
    Заполнения модели Ip, проверка на бан
    """
    def process_request(self, request, *args, **kwargs):
        ip = get_ip(request)
        user = str(request.user)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(user=user, ip=ip)
        else:
            ip = Ip.objects.filter(ip=ip).first()
            if ip.is_banned:
                context = {
                    'title': '403 Ошибка доступа.', 
                    'message': 'бан',
                }
                return render(request, 'error.html', context)
            
            ip.updated = now
            ip.save()
