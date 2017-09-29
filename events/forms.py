__author__ = 'OllyD'
from django import forms
from .models import EventModel
from django.contrib.admin.widgets import AdminDateWidget

class EventModelForm(forms.ModelForm):
    date = forms.DateField(
    widget=forms.TextInput(
        attrs={'id': 'datepicker'}
    )
)

    start_time = forms.TimeField(
    widget=forms.TextInput(
        attrs={'type': 'time'}
    )
)

    end_time = forms.TimeField(
    widget=forms.TextInput(
        attrs={'type': 'time'}
    )
)
    #start_time = forms.DateTimeField(widget=forms.SelectDateWidget())
    class Meta:
        model = EventModel
        fields = ['name', 'street_address', 'state', 'city', 'zipcode', 'description', 'picture', 'date', 'start_time', 'end_time']

