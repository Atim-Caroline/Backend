from django.apps import AppConfig

class ComplianceServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compliance_service'

    def ready(self):
        import compliance_service.signals  # noqa 