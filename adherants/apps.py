from django.apps import AppConfig


class AdherantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adherants'
    
    def ready(self):
        import adherants.signals
