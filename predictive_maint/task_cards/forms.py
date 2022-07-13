from django import forms
from datetime import datetime

from .models import *

class CreateTaskCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(CreateTaskCardForm, self).__init__(*args, **kwargs)
       self.fields['number'].initial = f'PREDMX-{datetime.now().strftime("%y%m%d%H%M")}'
    class Meta:
        model = TaskCard
        fields = '__all__'
        widgets = {
            'defect': forms.Select(attrs={'style': 'width: 150px'}),
            'description': forms.TextInput(attrs={'style': 'width: 100%'}),
        }

class CreateStepForm(forms.ModelForm):
    class Meta:
        model = TaskCardStep
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 3, 'class':"form-control mt-2 mb-3"}),
            'number': forms.NumberInput(attrs={"style": "width: 3em"}),
            'DELETE': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'image': forms.FileInput(attrs={"type": "file"}),
            
        }
        

class CreateMaterialForm(forms.ModelForm):
    class Meta:
        model = TaskCardMaterial
        fields = '__all__'
        widgets = {
            
        }

StepsFormSet = forms.inlineformset_factory(TaskCard, TaskCardStep, form=CreateStepForm, fields='__all__', extra=0) 
MaterialsFormSet = forms.inlineformset_factory(TaskCard, TaskCardMaterial, form=CreateMaterialForm, fields='__all__', extra=0) 