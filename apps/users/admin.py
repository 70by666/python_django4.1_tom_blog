from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение модели пользователей в админке
    """
    list_display = ('username', 'id', 'email')
    list_display_links = ('username',)
