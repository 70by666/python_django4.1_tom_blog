from django.contrib import admin

from apps.blog.models import BlogPosts


class BlogPostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'created', 'author')
    fields = (
        ('id', 'title', 'status', 'slug'), 
        ('created', 'updated'), 'author', 'updater'
        'image', ('short_descrtiprion', 'full_description'), 
    )
    readonly_fields = ('id', 'created')
