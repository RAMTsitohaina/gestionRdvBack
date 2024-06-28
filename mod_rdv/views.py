from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mod_rdv.models import Rdv
from mod_rdv.serializers import RdvSerializers

@api_view(['GET'])
@transaction.atomic
def get_rdv_filter(request):
    """
        DESC : Récupération filtrer des Rdv
    """
    queryset = Rdv.objects.all().order_by('date')

    # Initialisation des filtre
    query = Q()

    # Critère de recherche
    titre = request.query_params.get('titre', None)
    date = request.query_params.get('date', None)
    heure = request.query_params.get('heure', None)
    contact = request.query_params.get('contact', None)

    if titre is not None:
        query &= Q(titre__icontains = titre)
    
    if date is not None:
        query &= Q(date = date)

    if heure is not None:
        query &= Q(heure = heure)

    if contact is not None:
        query &= Q(contact__id = contact)

    if query :
        queryset = queryset.filter(query)

    return Response(RdvSerializers(queryset, many = True).data, status.HTTP_200_OK)

@api_view(['POST'])
@transaction.atomic
def create_rdv(request):
    """
        DESC : Création d'un Rdv
    """
    data = {
        'titre' : request.data['titre'],
        'date' : request.data['date'],
        'heure' : request.data['heure'],
        'contact' : request.data['contact'],
        'description' : None,
    }

    if 'description' in request.data.keys():
        data['description'] = request.data['description']

    serialized_data = RdvSerializers(data=data)

    if serialized_data.is_valid():

        rdv = Rdv.objects.create(
            titre = data['titre'],
            date = data['date'],
            heure = data['heure'],
            contact = data['contact'],
            description = data['description'],
        )

        return Response ("Rendez-vous enregistrer", status=status.HTTP_201_CREATED)
    
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@transaction.atomic
def update_rdv(request, pk):
    """
        DESC : Modification d'un rendez-vous
    """
    try:
        rdv = Rdv.objects.get(pk=pk)
    except Rdv.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialized_data = RdvSerializers(rdv, data = request.data)

    if serialized_data.is_valid():
        # Modification du contact
        rdv.titre = request.data['titre']
        rdv.date = request.data['date']
        rdv.heure = request.data['heure']
        rdv.contact = request.data['contact']

        if 'description' in request.data.keys():
            rdv.description = request.data['description']
        
        rdv.save()

        return Response('Rendez-vous modifié avec succès', status=status.HTTP_204_NO_CONTENT)
    
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@transaction.atomic
def delete_rdv(request, pk):
    """
        DESC : Suppression d'un Rendez-vous
    """
    try:
        rdv = Rdv.objects.get(pk=pk).delete()

        return Response("Rendez-vous supprimer", status=status.HTTP_204_NO_CONTENT)
    except Rdv.DoesNotExist:
        return Response('Rendez-vous non trouvé', status=status.HTTP_404_NOT_FOUND)
