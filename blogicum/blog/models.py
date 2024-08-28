from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseBlogModel


User = get_user_model()


class Category(BaseBlogModel):
    """Модель категории."""

    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        ),
        unique=True
    )

    class Meta(BaseBlogModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title', )

    def __str__(self) -> str:
        return self.title[:settings.REPRESENTATION_LENGTH]


class Location(BaseBlogModel):
    """Модель местоположения."""

    name = models.CharField(
        'Название места',
        max_length=settings.MAX_FIELD_LENGTH
    )

    class Meta(BaseBlogModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:settings.REPRESENTATION_LENGTH]


class Post(BaseBlogModel):
    """Модель поста."""

    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    image = models.ImageField('Картинка у публикации', blank=True)

    class Meta(BaseBlogModel.Meta):
        default_related_name = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:settings.REPRESENTATION_LENGTH]


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост'
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)
        default_related_name = 'comments'

    def __str__(self) -> str:
        return self.text[:settings.REPRESENTATION_LENGTH]
