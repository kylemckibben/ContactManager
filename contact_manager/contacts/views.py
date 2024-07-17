from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from contacts.models import Contact
from contacts.serializers import ContactSerializer


@csrf_exempt
def contact_list(request):
    """
    List all contacts, or create a new contact.
    """
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    

@csrf_exempt
def contact_detail(request, pk):
    """
    Read, Update, or Delete a contact.
    """
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ContactSerializer(contact, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        contact.delete()
        return HttpResponse(status=204)