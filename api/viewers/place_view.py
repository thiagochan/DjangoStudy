from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import Place
from api.serializers import PlaceSerializer
from api.services import place_service

@api_view(['GET', 'POST', 'PUT'])
def place_manager(request):
    if request.method == 'GET':
        places = Place.objects.all()

        serializer = PlaceSerializer(places, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        new_place = request.data

        serializer = PlaceSerializer(data=new_place)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    elif request.method == 'PUT':
        place_id = request.data['id']

        try:
            placeToUpdate = Place.objects.get(pk=place_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceSerializer(placeToUpdate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def place_by_id(request, place_id):
    if request.method == 'GET':
        place = Place.objects.get(pk=place_id)

        serializer = PlaceSerializer(place)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            place = place_service.get_place_by_id(place_id)
            place.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': f'Could not find place with id {place_id}'}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_400_BAD_REQUEST)