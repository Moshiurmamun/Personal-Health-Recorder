from django import forms
from .models import District
from .models import District

class DistrictForm(forms.Form):
    district = forms.ModelChoiceField(queryset=District.objects.all(), to_field_name='name')


