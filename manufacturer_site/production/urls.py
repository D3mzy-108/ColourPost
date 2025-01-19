from django.urls import path
from .views import (productions,
                    batch_details,
                    new_production,
                    add_package_item,
                    finish_production,
                    packaging_details,
                    delete_production,
                    production_details,
                    remove_package_item,
                    add_production_resource,
                    remove_production_resource,
                    navigate_production_environment)

urlpatterns = [
    path('', productions, name='productions'),
    path('new/', new_production, name='new_production'),
    path('delete/', delete_production, name='delete_production'),
    path('delete/', delete_production, name='delete_production'),
    path('<int:production_id>/navigate-environment/tab/<int:tab>/',
         navigate_production_environment, name='navigate_production_environment'),
    path('finish/<int:production_id>/',
         finish_production, name='finish_production'),

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
    path('<int:production_id>/packaging/add-item/',
         add_package_item, name='add_package_item'),
    path('packaging/remove-item/',
         remove_package_item, name='remove_package_item'),
]
