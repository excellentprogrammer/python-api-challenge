from rest_framework import generics
from rest_framework import serializers

from .models import Departure
from django.http import HttpResponse


class DepartureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departure
        fields = ('name', 'start_date', 'finish_date', 'category')

class DepartureView(generics.ListAPIView):
    queryset = Departure.objects.all()
    serializer_class = DepartureSerializer

import json

def load_fixtures(request):
    number_of_new_departure = 0;
    with open('departures.json') as json_data:
        departure_fixtures = json.load(json_data)
        for departure in departure_fixtures:
            if Departure.objects.filter(name=departure["name"], start_date=departure["start_date"], finish_date=departure["finish_date"], category=departure["category"]).count()==0:
                Departure(name=departure["name"], start_date=departure["start_date"], finish_date=departure["finish_date"],category=departure["category"]).save()
                number_of_new_departure += 1
    return HttpResponse( "%d new departures successfully inserted" % (number_of_new_departure))
