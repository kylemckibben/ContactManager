from django.urls import path
from contacts import views

app_name = "contacts"

urlpatterns = [
    path('contacts/', views.ContactList.as_view(), name='index'),
    path('contacts/<int:pk>/', views.ContactDetail.as_view(), name='detail'),
]