from rest_framework import serializers

from .models import Place, People

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    place = serializers.CharField(source='place.name', read_only=True)

    class Meta:
        model = People
        fields = ['name', 'place']

class PeopleCreateWithPlaceSerializer(serializers.ModelSerializer):
    place_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = People
        fields = ['name', 'place_id']