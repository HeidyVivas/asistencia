from django.apps import AppConfig

class AsistenciasConfig(AppConfig):
    name = 'asistencias'

    def ready(self):
        import asistencias.signals  # noqa
