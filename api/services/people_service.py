from api.models import People

def get_all_people():
    return People.objects.all()
    