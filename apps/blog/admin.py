from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.blog.models import Categories, Comments, Posts


@admin.register(Posts)
class BlogPostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'created', 'author')
    fields = (
        ('id', 'title', 'slug'), ('category', 'fixed'), 
        ('author', 'created'), ('updater', 'updated'),
        ('status', 'image', 'short_description'), 'full_description', 
    )
    readonly_fields = ('id', 'created', 'updated')


@admin.register(Categories)
class CategoriesAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)})
    )


@admin.register(Comments)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'post', 'author', 'created')
    mptt_level_indent = 2
    list_display_links = ('post',)
    list_filter = ('created', 'author')
