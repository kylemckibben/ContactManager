from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from contacts import views

app_name = "contacts"

urlpatterns = [
    path('contacts/', views.ContactList.as_view(), name='index'),
    path('contacts/<int:pk>/', views.ContactDetail.as_view(), name='detail'),
    path('users/', views.UserCreate.as_view(), name='register'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='profile'),
]


urlpatterns = format_suffix_patterns(urlpatterns)