from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from blog.models import Post


def post_all_query():
    """Вернуть все посты."""
    return (
        Post.objects.select_related(
            'category',
            'location',
            'author',
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )


def post_published_query():
    """Вернуть опубликованные посты."""
    return post_all_query().filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )


def get_post_data(pk):
    """Вернуть данные поста."""
    return get_object_or_404(
        Post,
        pk=pk,
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )
