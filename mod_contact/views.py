from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
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
    id = request.query_params.get('id', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    nom_prenom = request.query_params.get('nom_prenom', None)
    phone = request.query_params.get('phone', None)
    adresse = request.query_params.get('adresse', None)
    profession = request.query_params.get('profession', None)
    entreprise = request.query_params.get('entreprise', None)

    if id is not None:
        query &= Q(id = id)

    if nom is not None:
        query &= Q(nom__icontains = nom)
    
    if prenom is not None:
        query &= Q(prenom__icontains = prenom)

    if nom_prenom is not None:
        query &= Q(nom__icontains = nom_prenom) | Q(prenom__icontains = nom_prenom)

    if phone is not None:
        query &= Q(phone__icontains = phone)

    if adresse is not None:
        query &= Q(adresse__icontains = adresse)

    if profession is not None:
        query &= Q(profession__icontains = profession)

    if entreprise is not None:
        query &= Q(entreprise__icontains = entreprise)

    if query :
        queryset = queryset.filter(query)

    return Response(ContactSerializer(queryset, many = True).data, status.HTTP_200_OK)

@api_view(['POST'])
@transaction.atomic
def create_contact(request):
    """
        DESC : Création d'un contact
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
        DESC : Modification d'un contact
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

        return Response('Contact modifié avec succès', status=status.HTTP_200_OK)
    
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@transaction.atomic
def delete_contact(request, pk):
    """
        DESC : Suppression d'un contact
    """
    try:
        contact = Contact.objects.get(pk=pk).delete()

        return Response("Contact supprimer", status=status.HTTP_200_OK)
    except Contact.DoesNotExist:
        return Response('Contact non trouvé', status=status.HTTP_404_NOT_FOUND)
