from django.apps import AppConfig
from django.db.utils import OperationalError


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    
    def ready(self):
        try:
            from catalog.models import controls
            for c in controls.objects.filter(sort_id=None).all():
                c.set_sort_id()
                c.save()
        except OperationalError:
            # Database migration not yet completed, do nothing
            pass
