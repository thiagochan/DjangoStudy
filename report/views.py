from django.shortcuts import render
import io 
from django.http import FileResponse
from reportlab.pdfgen import canvas
from api.services import people_service
from api.services import place_service
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def all_people_report(request):
    people = people_service.get_all_people()

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, bottomup=0)
    p.drawString(50, 50, 'Pessoas:')

    xNow, yNow, xOffset, yOffset = [50, 75, 50, 25]
    for person in people:
        p.drawString(xNow, yNow, person.name)
        
        if (person.place != None):
            p.drawString(xNow + p.stringWidth(person.name) + xOffset, yNow, person.place.name)

        yNow += yOffset

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='all_people.pdf')

@api_view(['GET'])
def all_places_report(request):
    places = place_service.get_all_places()

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, bottomup=0)
    p.drawString(50, 50, 'Localizações:')

    xNow, yNow, xOffset, yOffset = [50, 75, 50, 25]
    for place in places:
        p.drawString(xNow, yNow, f'{place.name} possui {place.numPeopleNow} pessoas nesse momento.')

        yNow += yOffset
    
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='all_places.pdf')


@api_view(['GET'])
def test_report(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, bottomup=0)

    xNow, yNow, xOffset, yOffset = [50, 50, 10, 25]
    p.drawString(xNow, yNow, 'Asdrubaldo')
    p.drawString(xNow + p.stringWidth('Asdrubaldo') + xOffset, yNow, 'Biblioteca')
    p.drawString(xNow, yNow + yOffset, 'Asdrubaldo')
    p.drawString(xNow + xOffset, yNow + yOffset, 'Biblioteca')
    

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')