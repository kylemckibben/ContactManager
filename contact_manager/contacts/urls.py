from django.urls import path
from contacts import views

app_name = "contacts"

urlpatterns = [
    path('contacts/', views.contact_list, name='index'),
    path('contacts/<int:pk>/', views.contact_detail, name='detail'),
]