from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserCreationForm


class RegisterUser(CreateView, SuccessMessageMixin):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return response

    def get_success_message(self, cleaned_data):
        username = cleaned_data['username']
        return f'Добро пожаловать, {username}'
