from django.db import models


class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='contacts', on_delete=models.CASCADE)


    class Meta:
        ordering = ['last_name']