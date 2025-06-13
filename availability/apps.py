from django.apps import AppConfig


class AvailabilityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'availability'
    
    def ready(self):
        # Import and connect your signals
        import availability.signals