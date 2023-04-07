from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = 'apps.reports'
    verbose_name = 'Reports'

    def ready(self):
        import apps.reports.signals.handlers