import django_filters
from .models import FlightDetail
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'



class Flight(django_filters.FilterSet):

    class Meta:
        model = FlightDetail
        fields = ['FromLocation','ToLocation','DepartureTime',]
        #
        # widgets = {
        #     'FromLocation' : django_filters.
        # }




