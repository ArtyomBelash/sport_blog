from django.apps import AppConfig


class SportPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sport_posts'
    verbose_name = 'Спортиный Блог'

    def ready(self):
        from .signals import add_slug