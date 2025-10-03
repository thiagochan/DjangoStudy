from api.models import Place
from django.core.exceptions import ObjectDoesNotExist

class PlaceNotFound(Exception):
    pass

def get_all_places():
    return Place.objects.all()

def get_place_by_id(id):
    try:
        return Place.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise PlaceNotFound(f'Place with id {id} not found')