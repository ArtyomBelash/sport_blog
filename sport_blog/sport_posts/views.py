from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView, DeleteView
from .forms import *
from .models import *
from django.contrib.auth.models import User


class PostListView(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'spot_posts/index.html'
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).prefetch_related('cat', 'author')


class PostDetail(DetailView, FormView):
    model = Post
    context_object_name = 'post'
    template_name = 'spot_posts/detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'slug': self.get_object().slug})

    def form_valid(self, form):
        form = Comment.objects.create(author=self.request.user,
                                      body=form.cleaned_data['body'],
                                      post=self.get_object())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post__slug=self.kwargs['slug']).select_related('author')
        context['comments'] = comments
        count_com = comments.count()
        context['count_com'] = count_com
        if self.request.user.is_authenticated:
            bookmark = Bookmark.objects.filter(post=self.get_object(), user=self.request.user)
            if bookmark:
                context['bookmark'] = bookmark
        return context


class AddBookmark(CreateView):
    model = Post
    slug_field = 'post_slug'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        bookmark = Bookmark.objects.get_or_create(user=self.request.user, post=post)
        if bookmark:
            messages.success(request, 'Пост добавлен в закладки')
        return redirect('detail', slug=post.slug)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class RemoveBookmark(DeleteView):
    model = Post
    slug_field = 'post_slug'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        bookmark = Bookmark.objects.get(user=self.request.user, post=post)
        bookmark.delete()
        messages.success(request, 'Пост удален из закладок')
        return redirect('detail', slug=post.slug)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class BookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'spot_posts/bookmarks.html'
    context_object_name = 'bookmarks'
    login_url = '/users/login'

    def get_queryset(self):
        user = User.objects.get(username=self.request.user.username)
        return super().get_queryset().filter(user=user).select_related('post')


class AddPostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    fields = ('title', 'content', 'image', 'cat', 'video')
    model = Post
    success_url = reverse_lazy('index')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        title = cleaned_data['title']
        return f' Спасибо, {self.request.user.username}! Ваш пост "{title}" ' \
               f'будет добавлен, после того, как администратор его рассмотрит'


class CategoryView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "spot_posts/category.html"
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(cat__slug=self.kwargs['slug'], is_published=True).prefetch_related(
            'cat').select_related('author')


class SearchView(ListView):
    model = Post
    context_object_name = 'find_posts'
    template_name = 'spot_posts/search.html'
    ordering = ['-date']
    paginate_by = 3
    http_method_names = ['post', 'get']

    def get_queryset(self):
        search_query = self.request.GET.get('search1')
        if not search_query:
            search_query = self.request.session.get('last_search')
        self.request.session['last_search'] = search_query
        return super().get_queryset().filter(title__icontains=search_query, is_published=True).prefetch_related(
            'cat').select_related('author')


class AuthorPostView(ListView):
    model = Post
    context_object_name = 'authors'
    template_name = "spot_posts/authors.html"
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(author=self.kwargs['authors_id'], is_published=True).prefetch_related(
            'cat').select_related('author')
