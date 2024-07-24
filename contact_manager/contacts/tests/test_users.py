import json

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserCreateTests(TestCase):
    def test_create_new_user_success(self):
        """
        Creating a new user returns a 201 CREATED.
        """
        user = {
            'username': 'test_user',
            'password': 'test_pass',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(
            reverse('user-create'),
            data=(user),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_username_exists(self):
        """
        Attempting to create a user with an existing username returns a 400 BAD REQUEST.
        """
        User.objects.create(username='test_user')
        new_user = {
            'username': 'test_user',
            'password': 'test_pass',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(
            reverse('user-create'),
            data=(new_user),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDetailTests(TestCase):
    def test_get_user_authorized(self):
        """
        Getting own user info returns a 200 OK.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('user-detail', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_unauthorized(self):
        """
        Attempting to get not own user info returns a 403 FORBIDDEN.
        """
        not_user = User.objects.create(username='not_user')
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('user-detail', kwargs={'pk': not_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_authorized(self):
        """
        Updating own user infor returns a 204 NO CONTENT.
        """
        user = User.objects.create(username='test_user')
        user.set_password('test_pass')
        user.save()
        self.client.force_login(user=user)
        update_user = {
            'pk': user.pk,
            'username': user.username,
            'password': user.password,
            'first_name': 'Updated'
        }
        response = self.client.put(
            reverse('user-detail', kwargs={'pk': user.pk}),
            data=(update_user),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user_unauthorized(self):
        """
        Attempting to update not own user info returns a 403 FORBIDDEN.
        """
        not_user = User.objects.create(username='not_user')
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        response = self.client.put(
            reverse('user-detail', kwargs={'pk': not_user.pk}),
            data=({}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_authorized(self):
        """
        Deleting own profile returns a 204 NO CONTENT.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user)
        response = self.client.delete(
            reverse('user-detail', kwargs={'pk': user.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_unauthorized(self):
        """
        Attempting to delete not own profile returns a 403 FORBIDDEN.
        """
        not_user = User.objects.create(username='not_test_user')
        user = User.objects.create(username='test_user')
        self.client.force_login(user)
        response = self.client.delete(
            reverse('user-detail', kwargs={'pk': not_user.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)