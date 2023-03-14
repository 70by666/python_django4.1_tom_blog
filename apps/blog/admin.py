from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.blog.models import Categories, Posts


@admin.register(Posts)
class BlogPostsAdmin(admin.ModelAdmin):
    """
    Отображение модели блога в админке
    """
    
    list_display = ('title', 'id', 'status', 'created', 'author')
    fields = (
        ('id', 'title', 'slug', 'category'), 
        ('author', 'created'), ('updater', 'updated'),
        ('status', 'image', 'short_description'), 'full_description', 
    )
    readonly_fields = ('id', 'created', 'updated')


@admin.register(Categories)
class CategoriesAmin(DraggableMPTTAdmin):
    """
    Отображение модели категорий в админке
    """
    
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)})
    )
