from django.apps import AppConfig


class OuvragesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ouvrages'
    
    def ready(self):
        import ouvrages.signals
