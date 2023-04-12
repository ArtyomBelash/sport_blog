from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.fields import ReCaptchaV2Checkbox


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email '}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'data-size': 'normal', }), label='Я не робот')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'password1', 'password2', 'captcha',)


class AuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'data-size': 'compact', }),
                                                label='Я не робот')
