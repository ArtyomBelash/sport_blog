from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sport_posts.urls')),
    path('users/', include('users.urls')),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('', include('allauth.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
