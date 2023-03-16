from django.contrib import admin

from apps.users.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email')
    list_display_links = ('username',)


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'slug')
