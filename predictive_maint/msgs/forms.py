from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML, Row, Column
from crispy_forms.bootstrap import InlineCheckboxes

from .models import *


class OccurrencesDataRangeForm(forms.Form):
    """Form representing a range of date"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Column(Row(
                Column('from_date', css_class='col-2'),
                Column('to_date', css_class='col-2'),
          
                Column(Div(HTML("""
                <label class="mb-2">Fast daterange select</label>
                <br>
                <input type="button" value="3 months" id="3mInput" class="btn btn-secondary">
                <input type="button" value="1 month" id="1mInput" class="btn btn-secondary">
                <input type="button" value="2 weeks" id="2wInput" class="btn btn-secondary">
                <input type="button" value="1 week" id="1wInput" class="btn btn-secondary">
                <input type="button" value="3 days" id="3dInput" class="btn btn-secondary">
                """)), css_class = 'mt-0')
            ),
                Row(InlineCheckboxes('status')),
            ),
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    from_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control', 'style':'max-width: 9em'}))
    to_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control', 'style':'max-width: 9em'}))
    status = forms.ModelMultipleChoiceField(DefectStatus.objects.all(), widget=forms.CheckboxSelectMultiple(
        attrs={"class": "col", "type": "checkbox"}), label='Status', to_field_name="condition")


class CreateDefectForm(forms.ModelForm):
    
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