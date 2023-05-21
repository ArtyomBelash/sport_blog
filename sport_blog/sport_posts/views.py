from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
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
        return super().get_queryset().filter(is_published=True)


class PostDetail(DetailView, FormView, LoginRequiredMixin):
    model = Post
    context_object_name = 'post'
    template_name = 'spot_posts/detail.html'
    form_class = CommentForm
    login_url = '/users/login/'

    # success_url = reverse_lazy('detail')

    def get_queryset(self):
        return super().get_queryset().filter(slug=self.kwargs['slug'])

    def get_success_url(self):
        # return self.request.META.get('HTTP_REFERER', 'detail')  # ??????? Работает
        return reverse_lazy('detail', kwargs={'slug': Post.objects.get(slug=self.kwargs['slug']).slug})

    def form_valid(self, form):
        form = Comment.objects.create(author=self.request.user,
                                      body=form.cleaned_data['body'],
                                      post=Post.objects.get(slug=self.kwargs['slug']))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # первоначальный словарь
        context['comments'] = Comment.objects.filter(
            post=Post.objects.get(slug=self.kwargs['slug']))  # добавление в словарь по ключу
        context['count_com'] = len(context['comments'])
        if self.request.user.is_authenticated:
            bookmark = Bookmark.objects.filter(post=self.get_queryset()[0], user=self.request.user)
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

    def dispatch(self, request, *args, **kwargs):  # метод проверяет авторизован ли пользователь
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
        return super().get_queryset().filter(user=user)


class AddPostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    fields = ['title', 'content', 'image', 'cat', 'video']
    model = Post
    success_url = reverse_lazy('index')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user  # instance???
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
        return super().get_queryset().filter(cat__slug=self.kwargs['slug'], is_published=True)


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
        return super().get_queryset().filter(title__icontains=search_query, is_published=True)



class AuthorPostView(ListView):
    model = Post
    context_object_name = 'authors'
    template_name = "spot_posts/authors.html"
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(author=self.kwargs['authors_id'], is_published=True)
