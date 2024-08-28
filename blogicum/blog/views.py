from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Post, User

from blog.models import Post

from core.mixins import (
    CommentMixin,
    DispatchMixin,
    GetSuccessUrlPostDetail,
    GetSuccessUrlProfile,
    PostMixin
)
from core.utils import get_post_data, post_all_query, post_published_query


class IndexListView(ListView):
    """Главная страница со списком постов."""

    model = Post
    template_name = 'blog/index.html'
    queryset = post_published_query()
    paginate_by = settings.POSTS_BY_PAGE


class CategoryListView(IndexListView):
    """Страница со списком постов выбранной категории."""

    template_name = 'blog/category.html'
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class UserPostsListView(IndexListView):
    """Страница со списком постов пользователя."""

    template_name = 'blog/profile.html'
    author = None

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        if self.author == self.request.user:
            return post_all_query().filter(author=self.author)
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class PostDetailView(DetailView):
    """Страница выбранного поста."""

    model = Post
    template_name = 'blog/detail.html'
    post_data = None

    def get_queryset(self):
        self.post_data = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.post_data.author == self.request.user:
            return post_all_query().filter(pk=self.kwargs['pk'])
        return post_published_query().filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all().select_related(
            'author'
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя."""

    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class PostCreateView(
    PostMixin,
    GetSuccessUrlProfile,
    CreateView
):
    """Создание поста."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    PostMixin,
    DispatchMixin,
    GetSuccessUrlPostDetail,
    UpdateView
):
    """Редактирование поста."""

    form_class = PostForm


class PostDeleteView(
    PostMixin,
    DispatchMixin,
    GetSuccessUrlProfile,
    DeleteView
):
    """Удаление поста."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class CommentCreateView(
    CommentMixin,
    GetSuccessUrlPostDetail,
    CreateView
):
    """Написание комментария."""

    form_class = CommentForm
    post_data = None

    def dispatch(self, request, *args, **kwargs):
        self.post_data = get_post_data(self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_data
        return super().form_valid(form)


class CommentUpdateView(
    CommentMixin,
    DispatchMixin,
    GetSuccessUrlPostDetail,
    UpdateView
):
    """Редактирование комментария."""

    form_class = CommentForm
    pk_url_kwarg = 'comment_pk'


class CommentDeleteView(
    CommentMixin,
    DispatchMixin,
    GetSuccessUrlPostDetail,
    DeleteView
):
    """Удаление комментария."""

    pk_url_kwarg = 'comment_pk'
