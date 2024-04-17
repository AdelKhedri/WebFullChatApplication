from django.apps import AppConfig


class ChatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatapp'

    def ready(self):
        from .singals import create_uuid_unique