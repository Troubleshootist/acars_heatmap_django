from dataclasses import fields
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row, Column

from .models import *

class CreateDefect(forms.ModelForm):
    class Meta:
        model = Defect
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
            'action': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('plane'),
                    Column('reference'),
                    Column('status')
                ),
                Row(
                    Column('description'),
                    Column('action'),  
                ),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

class CreateDefectByMessageForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Div(
                Row('reference'),
                Row('description'),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))
        
    class Meta:
        model = Defect
        exclude = ('plane', 'status', 'action')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }



class EditDefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        exclude = ('plane',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
            'action': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Div(
                Row('reference'),
                Row(
                    Column('description'),
                    Column('action'),  
                ),
                Row('status')
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))