from django.contrib import admin

from apps.users.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение модели пользователей в админке
    """
    list_display = ('username', 'id', 'email')
    list_display_links = ('username',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    Отображение модели для верификации почты в админке
    """
    readonly_fields = ('expiration',)
