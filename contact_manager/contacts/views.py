from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from contacts.models import Contact
from contacts.permissions import IsOwner, IsUser
from contacts.serializers import ContactSerializer, UserSerializer

    
class ContactList(generics.ListCreateAPIView):
    """
    List all contacts, or Create a new contact.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class ContactDetail(generics.RetrieveDestroyAPIView):
    """
    Read, Update, or Delete a contact.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, *args, **kawrgs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class UserCreate(generics.CreateAPIView):
    """
    Create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    """
    Read, Update, or Delete a user. 
    """
    permission_classes = [permissions.IsAuthenticated, IsUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
    def put(self, request, *args, **kawrgs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
