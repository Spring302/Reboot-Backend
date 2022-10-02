from django.apps import AppConfig
from rec.jobs import updater


class RecConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rec'

    def ready(self):
        updater.start()
