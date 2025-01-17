from django.urls import path
from .views import productions

urlpatterns = [
    path('', productions, name='productions'),
]
