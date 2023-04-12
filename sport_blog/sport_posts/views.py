from django.contrib import messages
# from django.contrib.auth.decorators import login_required
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


# def add_bookmark(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     bookmark = Bookmark.objects.get_or_create(user=request.user, post=post)
#     if bookmark:
#         messages.success(request, 'Пост добавлен в закладки')
#         print(bookmark)
#     return redirect('detail', slug=post.slug)


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


# def remove_bookmark(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     bookmark = Bookmark.objects.get(user=request.user, post=post)
#     bookmark.delete()
#     messages.success(request, 'Пост удален из закладок')
#     return redirect('detail', slug=post.slug)


# def bookmarks(request):
#     user = User.objects.get(username=request.user.username)
#     bookmarks = Bookmark.objects.filter(user=user)
#     return render(request, 'spot_posts/bookmarks.html', {'bookmarks': bookmarks})


class BookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'spot_posts/bookmarks.html'
    context_object_name = 'bookmarks'
    login_url = '/users/login'

    def get_queryset(self):
        user = User.objects.get(username=self.request.user.username)
        return super().get_queryset().filter(user=user)


#

# def detail(request, slug):
#     post = Post.objects.get(slug=slug)
#     form = CommentForm()
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             user = User.objects.get(username=request.user.username)
#             comment = Comment(
#                 author=user,
#                 body=form.cleaned_data['body'],
#                 post=post)
#             comment.save()
#             form.cleaned_data.clear()
#     comments = Comment.objects.filter(post=post)
#     count_com = len(comments)
#     cont = {
#         'comments': comments,
#         'count_com': count_com,
#         'post': post,
#         'form': form,
#
#     }
#     return render(request, 'spot_posts/detail.html', cont)


# @login_required
# def add_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid() and User.is_authenticated:
#             user = User.objects.get(username=request.user.username)
#             print(user)
#             cats = form.cleaned_data.get('cat')
#             post = Post(title=form.cleaned_data['title'],
#                         image=form.cleaned_data['image'],
#                         slug=form.cleaned_data['slug'],
#                         video=form.cleaned_data['video'],
#                         content=form.cleaned_data['content'],
#                         author=user)
#             post.save()
#             for cat in cats:
#                 post.cat.add(cat)
#             messages.success(request, 'Ваш пост добавлен')
#             return redirect('/')
#     else:
#         form = PostForm()
#     return render(request, 'users/add_post.html', {'form': form})


class AddPostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    fields = ['title', 'content', 'image', 'cat', 'video']
    model = Post
    success_url = reverse_lazy('index')
    login_url = '/users/login/'

    # success_message = 'Ваш пост добавлен'

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
    http_method_names = ['post', ]

    def get_queryset(self):
        if self.request.method == 'POST':
            return super().get_queryset().filter(title__icontains=self.request.POST.get('search1'), is_published=True)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class AuthorPostView(ListView):
    model = Post
    context_object_name = 'authors'
    template_name = "spot_posts/authors.html"
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(author=self.kwargs['authors_id'], is_published=True)
