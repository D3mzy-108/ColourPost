from django.urls import path
from .views import productions, new_production, delete_production, production_details, add_production_resource, remove_production_resource

urlpatterns = [
    path('', productions, name='productions'),
    path('new/', new_production, name='new_production'),
    path('delete/', delete_production, name='delete_production'),
    path('<int:production_id>/details/',
         production_details, name='production_details'),
    path('<int:production_id>/add-resources/',
         add_production_resource, name='add_production_resource'),
    path('remove-resources/',
         remove_production_resource, name='remove_production_resource'),
]
