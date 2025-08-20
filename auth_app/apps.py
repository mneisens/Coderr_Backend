from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        import auth_app.signals
