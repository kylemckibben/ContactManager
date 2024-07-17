import json

from django.forms.models import model_to_dict
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from contacts.models import Contact

def create_contact(first_name: str, last_name: str, email: str='', phone: str='', notes: str='') -> Contact:
    """
    Create a contact with given fields to use for testing, using current time for 'created' field.

    Params:
        first_name (required): contact's first name
        last_name (required): contact's last name
        email: contact's email address
        phone: contact's phone number; supports up to 14 characters, ex (###)-###-####
        notes: addition information about the contact
    
    Return:
        a Contact model object
    """
    time = timezone.now()
    return Contact.objects.create(
        created=time, 
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
        contact_1 = create_contact(
            first_name='user1', 
            last_name='user1', 
            email='user1@test.com', 
            phone='1234567890')
        contact_2 = create_contact(
            first_name='user2', 
            last_name='user2', 
            notes='Oops, forgot their number')
        contacts = [contact_1, contact_2]
        response = self.client.get(
            reverse('contacts:index'), 
            args=(contacts))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_contact_success(self):
        """
        A contact with at least the first and last name provided returns a 200 OK.
        """
        contact = create_contact(
            first_name='first', 
            last_name='last')
        data = json.dumps(model_to_dict(contact))
        response = self.client.post(
            reverse('contacts:index'), 
            data=(data), 
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_contact_failure(self):
        """
        A contact missing the first or last name returns a 400 BAD REQUEST.
        """
        contact = create_contact(
            first_name='', 
            last_name='last')
        data = json.dumps(model_to_dict(contact))
        response = self.client.post(
            reverse('contacts:index'), 
            data=(data), 
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        


class ContactDetailViewTests(TestCase):
    def test_contact_exists(self):
        """
        Retrieving an existing contact returns a 200 OK
        """
        contact = create_contact(
            first_name='first', 
            last_name='last')
        response = self.client.get(
            reverse('contacts:detail', kwargs={'pk':contact.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contact_dne(self):
        """
        Retrieving a contact that does not exist returns a 404 NOT FOUND
        """
        response = self.client.get(
            reverse('contacts:detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contact_updatable(self):
        """
        Updating a contact returns a 204 NO CONTENT
        """
        contact = create_contact(first_name='first', last_name='last')
        update_contact = {
            'pk': 1,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'update@email.com'
        }
        response = self.client.put(
            reverse('contacts:detail', kwargs={'pk': contact.pk}),
            data=update_contact,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_contact_delete(self):
        """
        Deleting a contact returns a 204 NO CONTENT
        """
        contact = create_contact(first_name='first', last_name='last')
        response = self.client.delete(
            reverse('contacts:detail', kwargs={'pk': contact.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)