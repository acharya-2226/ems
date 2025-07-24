from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core Application'  # Better admin display name
    
    def ready(self):
        """
        Called when Django starts up.
        Register signals and perform any initialization.
        """
        try:
            import core.signals  # This will register signals
        except ImportError:
            # Handle case where signals.py might be missing or have import errors
            pass