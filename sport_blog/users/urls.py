from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import AuthenticationForm
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, form_class=AuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
