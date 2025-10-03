from django.urls import path

from . import views

urlpatterns = [
    path('people/', view=views.people_view.people_manager),
    path('people/<int:people_id>/', view=views.people_view.people_by_id),
    path('place/', view=views.place_view.place_manager),
    path('place/<int:place_id>/', view=views.place_view.place_by_id),
]
