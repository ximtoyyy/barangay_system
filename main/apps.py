from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        from . import checks  # noqa  (registers the MySQL-only safety check)
