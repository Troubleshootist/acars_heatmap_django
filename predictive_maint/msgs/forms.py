from django import forms

class OccurrencesDataRangeForm(forms.Form):
    """Form representing a range of date"""
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
