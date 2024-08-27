from django.contrib import admin

from .models import Category, Location, Post

from core.admin import BlogAdmin, CommentAdmin


admin.site.empty_value_display = '-пусто-'


class CategoryAdmin(BlogAdmin):
    list_display = (
        'title',
        'is_published',
        'created_at',
        'slug',
    )
    list_display_links = ('title',)


class LocationAdmin(BlogAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_display_links = ('name',)


class PostAdmin(BlogAdmin):
    inlines = [CommentAdmin]
    list_display = (
        'title',
        'author',
        'pub_date',
        'is_published',
    )
    list_display_links = ('title',)
    list_filter = (
        'is_published',
        'category',
        'location',
        'author',
    )
    search_fields = (
        'title',
        'text',
    )
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
