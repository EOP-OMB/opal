from django.apps import AppConfig
import os
from django.conf import settings

class ssp(AppConfig):
    name = 'ssp'
    path = os.path.join(settings.BASE_DIR, 'ssp')

    def ready(self):
        import ssp.signals

