from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from contacts import views

urlpatterns = format_suffix_patterns([
    path('contacts/', 
         views.ContactList.as_view(), 
         name='contact-list'),
    path('contacts/<int:pk>/', 
         views.ContactDetail.as_view(), 
         name='contact-detail'),
    path('users/', 
         views.UserCreate.as_view(), 
         name='user-create'),
    path('users/<int:pk>/', 
         views.UserDetail.as_view(), 
         name='user-detail'),
])