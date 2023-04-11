from django.contrib import admin

from apps.users.models import (EmailVerification, Ip, ProfileComments,
                               Subscription, User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email')
    list_display_links = ('username',)
    readonly_fields = ('password',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    readonly_fields = ('expiration',)


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


@admin.register(ProfileComments)
class CommentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'created')
    list_display_links = ('user',)
    list_filter = ('created', 'author')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user',)
