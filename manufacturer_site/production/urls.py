from django.urls import path
from .views import productions, new_production, delete_production, production_details, add_production_resource, remove_production_resource, batch_details, packaging_details

urlpatterns = [
    path('', productions, name='productions'),
    path('new/', new_production, name='new_production'),
    path('delete/', delete_production, name='delete_production'),

    # PRODUCTION DETAILS
    path('<int:production_id>/details/',
         production_details, name='production_details'),
    path('<int:production_id>/add-resources/',
         add_production_resource, name='add_production_resource'),
    path('remove-resources/',
         remove_production_resource, name='remove_production_resource'),

    # BATCH URLS
    path('<int:production_id>/batch-details/',
         batch_details, name='batch_details'),

    # PACKAGING URLS
    path('<int:production_id>/packaging/',
         packaging_details, name='packaging_details'),
]
