from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row, Column

from .models import *

class CreateTaskCardForm(forms.ModelForm):
    class Meta:
        model = TaskCard
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(

        )

class CreateStepForm(forms.ModelForm):
    class Meta:
        model = TaskCardStep
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 3, 'class':"form-control mt-2 mb-3"}),
            'number': forms.NumberInput(attrs={"style": "width: 3em"}),
            'DELETE': forms.CheckboxInput(attrs={"class": "form-check-input"})
            
        }


TaskCardFormSet = forms.inlineformset_factory(TaskCard, TaskCardStep, form=CreateStepForm, fields='__all__', extra=0) 