from django.contrib import admin

from blog.models import Comment


class BlogAdmin(admin.ModelAdmin):
    """Общий интерфейс админ-панели."""

    list_editable = ('is_published',)
    list_filter = ('created_at',)


class CommentAdmin(admin.TabularInline):
    """Интерфейс комментариев."""

    model = Comment
    readonly_fields = (
        'text',
        'author',
        'created_at',
    )
    extra = 0
