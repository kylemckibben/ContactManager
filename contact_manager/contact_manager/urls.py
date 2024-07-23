
from django.urls import include, path

urlpatterns = [
    path('', include('contacts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
