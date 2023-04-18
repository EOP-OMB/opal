from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import catalog_index_view, catalog_list_view, catalog_detail_view, import_catalog_view, control_detail_view, load_controls, load_statements, load_params

app_name = 'catalog'
urlpatterns = [path('', catalog_index_view, name='catalog_index_view'),
               path('list', catalog_list_view.as_view(), name='catalog_list_view'),
               path('<int:pk>', cache_page(60 * 15)(catalog_detail_view.as_view()), name='catalog_detail_view'),
               path('import/<str:catalog_id>', import_catalog_view, name='import_catalog_view'),
               path('control/<int:pk>', control_detail_view.as_view(), name='control_detail_view'),
               path('ajax/load-controls/', load_controls, name='ajax_load_controls'),
               path('ajax/load_statements/', load_statements, name='ajax_load_statements'),
               path('ajax/load_params/', load_params, name='ajax_load_params'),
               ]
