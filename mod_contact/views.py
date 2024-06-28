from django.shortcuts import render
from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from mod_contact.models import Contact
from mod_contact.serializers import ContactSerializer

@api_view(['GET'])
@transaction.atomic
def get_contact_filter(request):
    """
        DESC : Récupération filtrer des contacts
    """
    queryset = Contact.objects.all().order_by('nom')

    # Initialisation des filtre
    query = Q()

    # Critère de recherche
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    nom_prenom = request.query_params.get('nom_prenom', None)
    phone = request.query_params.get('phone', None)
    adresse = request.query_params.get('adresse', None)
    profession = request.query_params.get('profession', None)
    entreprise = request.query_params.get('entreprise', None)

    if nom is not None:
        query &= Q(nom = nom)
    
    if prenom is not None:
        query &= Q(prenom = prenom)

    if nom_prenom is not None:
        query &= Q(nom__contains = nom_prenom) | Q(prenom__contains = nom_prenom)

    if phone is not None:
        query &= Q(phone = phone)

    if adresse is not None:
        query &= Q(adresse = adresse)

    if profession is not None:
        query &= Q(profession = profession)

    if entreprise is not None:
        query &= Q(entreprise = entreprise)

    if query :
        queryset = queryset.filter(query)

    return Response(ContactSerializer(queryset, many = True).data, status.HTTP_200_OK)

@api_view(['POST'])
@transaction.atomic
def create_contact(request):
    """
        Création d'un contact
    """

    data = {
        'nom' : request.data['nom'],
        'prenom' : request.data['prenom'],
        'phone' : request.data['phone'],
        'adresse' : request.data['adresse'],
        'profession' : None,
        'enterprise' : None,
    }

    if 'profession' in request.data.keys():
        data['profession'] = request.data['profession']
    
    if 'entreprise' in request.data.keys():
        data['entreprise'] = request.data['entreprise']
    
    serialized_data = ContactSerializer(data=data)

    if serialized_data.is_valid():

        contact = Contact.objects.create(
            nom = data['nom'],
            prenom = data['prenom'],
            phone = data['phone'],
            adresse = data['adresse'],
            profession = data['profession'],
            entreprise = data['entreprise']
        )

        return Response ("Contact enregistrer", status=status.HTTP_201_CREATED)

    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@transaction.atomic
def update_contact(request, pk):
    """
        DESC : Modification d'un contac
    """
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialized_data = ContactSerializer(contact, data = request.data)

    if serialized_data.is_valid():
        # Modification du contact
        contact.nom = request.data['nom']
        contact.prenom = request.data['prenom']
        contact.phone = request.data['phone']
        contact.adresse = request.data['adresse']

        if 'profession' in request.data.keys():
            contact.profession = request.data['profession']
    
        if 'entreprise' in request.data.keys():
            contact.entreprise = request.data['entreprise']
        
        contact.save()

        return Response('contact modifié avec succès', status=status.HTTP_204_NO_CONTENT)
    
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@transaction.atomic
def delete_contact(request, pk):
    """
        DESC : Suppression d'un contact
    """
    try:
        contact = Contact.objects.get(pk=pk).delete()

        return Response("Contact supprimer", status=status.HTTP_204_NO_CONTENT)
    except Contact.DoesNotExist:
        return Response('Contact non trouvé', status=status.HTTP_404_NOT_FOUND)
