from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


from contacts.models import Contact
from contacts.permissions import IsOwner, IsUser
from contacts.serializers import ContactSerializer, UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
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
    

@method_decorator(csrf_exempt, name='dispatch')   
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
    

@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(generics.GenericAPIView):
    """
    Handle user login.
    """
    serializer_class = ObtainAuthToken.serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id': user.pk,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreate(generics.CreateAPIView):
    """
    Create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
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
    

@method_decorator(csrf_exempt, name='dispatch')
class UserExists(generics.GenericAPIView):
    """
    Check if a username or email already exists.
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        # username = request.data.get('username', None)
        # email = request.data.get('email', None)

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)

