
from django.urls import include, path
from contacts.views import UserLogin

urlpatterns = [
    path('api/', include('contacts.urls')),
    path('api-auth/login/', UserLogin.as_view(), name='user-login'),
    path('api-auth/', include('rest_framework.urls')),
]
