from django.contrib import admin

from apps.users.models import EmailVerification, Ip, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение модели пользователей в админке
    """
    list_display = ('username', 'id', 'email')
    list_display_links = ('username',)
    readonly_fields = ('password',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    Отображение модели для верификации почты в админке
    """
    readonly_fields = ('expiration',)


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    """
    Отображение модели Ip в админке
    """
    readonly_fields = ('created', 'updated')
