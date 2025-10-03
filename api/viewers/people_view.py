from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.services import place_service
from api.models import People
from api.serializers import PeopleSerializer, PeopleCreateWithPlaceSerializer

@api_view(['GET', 'POST', 'PUT'])
def people_manager(request):
    if request.method=='GET':
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)

        return Response(data=serializer.data)
    
    elif request.method=='POST':
        new_people = request.data

        serializer = PeopleCreateWithPlaceSerializer(data=new_people)
        if serializer.is_valid():
            place_id = serializer.validated_data.get('place_id')
            
            try:
                place = place_service.get_place_by_id(place_id)
                place.numPeopleNow += 1
                place.save()
            except place_service.PlaceNotFound as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
    elif request.method == 'PUT':
        people_id = request.data['id']

        try:
            peopleToUpdate = People.objects.get(pk=people_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        place_id = request.data.get('place_id')

        try:                
            if (peopleToUpdate.place != None and peopleToUpdate.place.pk != None): # se tiver local antigo valido
                oldPlace = place_service.get_place_by_id(peopleToUpdate.place.pk)

                oldPlace.numPeopleNow -= 1
                oldPlace.save()

            if (place_id != None):
                newPlace = place_service.get_place_by_id(place_id)
                if (newPlace != None):
                    newPlace.numPeopleNow += 1
                    newPlace.save()

        except:
            return Response({"error": f'Place with id {place_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PeopleCreateWithPlaceSerializer(peopleToUpdate, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def people_by_id(request, people_id):
    if request.method=='GET':
        try:
            people = People.objects.get(pk=people_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PeopleSerializer(people)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            people = People.objects.get(pk=people_id)

            if (people.place != None):
                try:
                    place = place_service.get_place_by_id(people.place.pk)
                    place.numPeopleNow -= 1
                    place.save()
                except place_service.PlaceNotFound as e:
                    return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

            people.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={'error': f'Person with with id {people_id} not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
        

