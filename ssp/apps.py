from django.apps import AppConfig


class ssp(AppConfig):
    name = 'ssp'

    def ready(self):
        import ssp.signals

