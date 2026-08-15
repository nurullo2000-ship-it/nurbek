"""
Core app configuration
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Негизги функциялар'

    def ready(self):
        """Import signals when app is ready"""
        import apps.core.signals  # noqa
