from django import forms
from .models import *


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'style': 'resize:none',
                'class': 'form-control',
                'placeholder': 'Коментарии могут оставлять только авторизованные пользователи'
            }
        )
    )


# class PostForm(forms.Form):
# title = forms.CharField(max_length=255, widget=forms.TextInput, label='Заголовок', help_text='Введите заголовок')
# content = forms.CharField(widget=forms.Textarea(attrs={
#     'placeholder': 'Контент',
# }), label='Статья')
# slug = forms.SlugField(max_length=250, label='URL')
# cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='------')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'cat', 'slug']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 148, 'rows': 10})
        }
