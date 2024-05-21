from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='a_post')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    image = models.ImageField(upload_to='sport', blank=True, verbose_name='Картинка')
    video = EmbedVideoField(verbose_name='Видео URL', blank=True)
    cat = models.ManyToManyField('Category', verbose_name="Категории")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})  # имя url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Category(models.Model):
    name_cat = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')

    def __str__(self):
        return self.name_cat

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Автор: {self.author} - {self.post}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.post.title}'

    class Meta:
        unique_together = ('user', 'post')
