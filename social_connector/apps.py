from django.apps import AppConfig

class SocialConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_connector'

    def ready(self):
        import social_connector.signals  # noqa 