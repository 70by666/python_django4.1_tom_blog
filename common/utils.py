from uuid import uuid4

from pytils.translit import slugify


def unique_slug(instance, title):
    """
    Функция для генерации случайного slug
    """
    model = instance.__class__
    slug = slugify(title)
    while model.objects.filter(slug=slug).exists():
        slug = f'{slug}-{uuid4().hex[:8]}'
        
    return slug
