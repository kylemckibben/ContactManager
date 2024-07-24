import json

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from contacts.models import Contact


def create_contact(first_name: str, last_name: str, owner: User, email: str='', phone: str='', notes: str='') -> Contact:
    """
    Create a contact with given fields to use for testing, using current time for 'created' field.

    Params:
        first_name (required): contact's first name
        last_name (required): contact's last name
        email: contact's email address
        phone: contact's phone number; supports up to 14 characters, ex (###)-###-####
        notes: addition information about the contact
        owner: who the contact belongs to
    
    Return:
        a Contact model object
    """
    time = timezone.now()

    return Contact.objects.create(
        created=time, 
        owner=owner,
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        phone=phone, 
        notes=notes)


class ContactListViewTests(TestCase):
    def test_get_contacts_list(self):
        """
        A list of valid contacts returns a 200 OK.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        contact_1 = create_contact(
            first_name='user1', 
            last_name='user1', 
            email='user1@test.com', 
            phone='1234567890',
            owner=user)
        contact_2 = create_contact(
            first_name='user2', 
            last_name='user2', 
            notes='Oops, forgot their number',
            owner=user)
        contacts = [contact_1, contact_2]
        response = self.client.get(
            reverse('contact-list'), 
            args=(contacts))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_contact_success(self):
        """
        A contact with at least the first and last name provided returns a 200 OK.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        contact = create_contact(
            first_name='first', 
            last_name='last',
            owner=user)
        data = json.dumps(model_to_dict(contact))
        response = self.client.post(
            reverse('contact-list'), 
            data=(data), 
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_contact_failure(self):
        """
        A contact missing the first or last name returns a 400 BAD REQUEST.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        contact = create_contact(
            first_name='', 
            last_name='last',
            owner=user)
        data = json.dumps(model_to_dict(contact))
        response = self.client.post(
            reverse('contact-list'), 
            data=(data), 
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        


class ContactDetailViewTests(TestCase):
    def test_contact_exists(self):
        """
        Retrieving an existing contact returns a 200 OK.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        contact = create_contact(
            first_name='first', 
            last_name='last',
            owner=user)
        response = self.client.get(
            reverse('contact-detail', kwargs={'pk':contact.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contact_dne(self):
        """
        Retrieving a contact that does not exist returns a 404 NOT FOUND.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('contact-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contact_not_owned_by(self):
        ...

    def test_contact_updatable(self):
        """
        Updating a contact returns a 204 NO CONTENT.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        contact = create_contact(
            first_name='first', 
            last_name='last',
            owner=user)
        update_contact = {
            'pk': contact.pk,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'update@email.com',
            'owner': json.dumps(contact.owner, default=str)
        }
        response = self.client.put(
            reverse('contact-detail', kwargs={'pk': contact.pk}),
            data=(update_contact),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_contact_updatable_not_owned(self):
        """
        Attempting to update a contact not owned returns a 403 FORBIDDEN.
        """
        not_user = User.objects.create(username='not_test_user')
        user = User.objects.create(username='test_user')
        contact = create_contact(
            first_name='first', 
            last_name='last',
            owner=not_user)
        update_contact = {
            'pk': contact.pk,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'update@email.com'
        }
        self.client.force_login(user=user)
        response = self.client.put(
            reverse('contact-detail', kwargs={'pk': contact.pk}),
            data=(update_contact),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contact_delete(self):
        """
        Deleting a contact returns a 204 NO CONTENT.
        """
        user = User.objects.create(username='test_user')
        self.client.force_login(user=user)
        contact = create_contact(
            first_name='first', 
            last_name='last',
            owner=user)
        response = self.client.delete(
            reverse('contact-detail', kwargs={'pk': contact.pk}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_contact_delete_not_owned(self):
        """
        Attempting to delete a contact not owned returns a 403 FORBIDDEN.
        """
        not_user = User.objects.create(username='not_test_user')
        user = User.objects.create(username='test_user')
        contact = create_contact(
            first_name='first', 
            last_name='last',
            owner=not_user)
        self.client.force_login(user=user)
        response = self.client.delete(
            reverse('contact-detail', kwargs={'pk': contact.pk}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)