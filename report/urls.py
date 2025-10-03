from django.urls import path, include

from . import views

urlpatterns = [
    path('', view=views.test_report),
    path('people/', view=views.all_people_report),
    path('place/', view=views.all_places_report),
]