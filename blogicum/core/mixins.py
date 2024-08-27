from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from blog.models import Comment, Post


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'


class PostMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'


class DispatchMixin:

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class GetSuccessUrlPostDetail:

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:post_detail', kwargs={'pk': pk})


class GetSuccessUrlProfile:
    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('blog:profile', kwargs={'username': username})
