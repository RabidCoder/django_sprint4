from django.forms import DateTimeInput, ModelForm, Textarea
from django.utils import timezone

from .models import Comment, Post, User


class CommentForm(ModelForm):
    """Форма редактирования комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': Textarea({'rows': '3'})}


class PostForm(ModelForm):
    """Форма редактирования поста."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'image',
            'location',
            'category',
            'pub_date',
        )
        widgets = {
            'pub_date': DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}
            ),
            'text': Textarea({'rows': '5'})
        }


class ProfileForm(ModelForm):
    """Форма редактирования информации о пользователе."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
