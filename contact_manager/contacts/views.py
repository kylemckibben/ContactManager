from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from contacts.models import Contact
from contacts.serializers import ContactSerializer

    
class ContactList(generics.ListCreateAPIView):
    """
    List all contacts, or create a new contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    
class ContactDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Read, Update, or Delete a contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
        
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, pk, format=None):
        try:
            contact = Contact.objects.get(pk=pk)
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            raise Http404
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)