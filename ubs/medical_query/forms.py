from django import forms
from dal import autocomplete
from .models import *

class MedicalQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        exclude = ['medical','date']
        fields= "__all__"

# Formulario para details
class MedicalQueryAttendanceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
       super(MedicalQueryAttendanceForm, self).__init__(*args, **kwargs)

       self.fields['main_complaint'].widget.attrs['readonly'] = True
       self.fields['current_health_history'].widget.attrs['readonly'] = True
       self.fields['review_of_systems'].widget.attrs['readonly'] = True
       self.fields['epidemiological_history'].widget.attrs['readonly'] = True
       self.fields['previous_pathological_history'].widget.attrs['readonly'] = True
       self.fields['family_history'].widget.attrs['readonly'] = True
       self.fields['physiological_personal_antecedents'].widget.attrs['readonly'] = True
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['diagnostic_hypotheses'].widget.attrs['readonly'] = True
       self.fields['take_duct'].widget.attrs['readonly'] = True

       self.fields['pa_exam'].widget.attrs['readonly'] = True
       self.fields['p_exam'].widget.attrs['readonly'] = True
       self.fields['fc_exam'].widget.attrs['readonly'] = True
       self.fields['fr_exam'].widget.attrs['readonly'] = True
       self.fields['tax_exam'].widget.attrs['readonly'] = True
       self.fields['peso_exam'].widget.attrs['readonly'] = True
       self.fields['heigth_exam'].widget.attrs['readonly'] = True

    
    class Meta:
        model = Query
        exclude = ['medical','date','patient']
        fields= "__all__"
