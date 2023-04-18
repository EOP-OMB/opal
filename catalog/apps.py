from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    
    def ready(self):
        from catalog.models import controls
        for c in controls.objects.filter(sort_id=None).all():
            c.set_sort_id()
            c.save()
