from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'is_published', 'date', 'image', 'slug')
    list_editable = ('is_published',)


class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name_cat',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CatAdmin)
admin.site.register(Comment)
