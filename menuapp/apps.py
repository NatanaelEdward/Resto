from django.apps import AppConfig

class MenuappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menuapp'

    def ready(self):
        import menuapp.signals  # Import your signals module here
