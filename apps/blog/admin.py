from django.contrib import admin

from apps.blog.models import BlogPosts


@admin.register(BlogPosts)
class BlogPostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'created', 'author')
    fields = (
        ('id', 'title', 'slug'), 
        ('author', 'created'), ('updater', 'updated'),
        ('status', 'image', 'short_descrtiprion'), 'full_description', 
    )
    readonly_fields = ('id', 'created', 'updated')
