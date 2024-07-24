from django.contrib.auth.models import User
from rest_framework import serializers

from contacts.models import Contact


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Contact
        fields = ['owner', 'id', 'first_name', 'last_name', 'email', 'phone', 'notes']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    contacts = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='contact-detail', 
        read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data and validated_data['password'] != instance.password:
            password = validated_data.pop('password', None)
            instance.set_password(password)
        return super().update(instance, validated_data)
        

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'contacts']