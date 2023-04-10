from apps.users.models import Ip
from services.utils import get_ip
from tom_blog.tasks import send_telegram_message_task


def ban(request, data=None):
    """
    Забанить
    """
    ip = get_ip(request)
    send_telegram_message_task.delay(ip=ip)
    ip = Ip.objects.get(ip=ip)
    ip.is_banned = True
    ip.save()
