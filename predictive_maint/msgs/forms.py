from django import forms
from .models import *


class OccurrencesDataRangeForm(forms.Form):
    """Form representing a range of date"""
    from_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    to_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    status = forms.ModelMultipleChoiceField(DefectStatus.objects.all(), widget=forms.CheckboxSelectMultiple(
        attrs={"class": "d"}), label='Status', to_field_name="condition")
    
    
