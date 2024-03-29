from django import forms
from dal import autocomplete
from .models import *

class MedicalQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields= [
            'type_query','main_complaint',
            'current_health_history','review_of_systems',
            'epidemiological_history','previous_pathological_history',
            'family_history','physiological_personal_antecedents',
            'summary','diagnostic_hypotheses','take_duct'
        ]

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

    class Meta:
        model = Query
        exclude = ['medical','date','patient','PhisicalExam_idPhisicalExam','type_query','User_idUser','Patient_idPatient']
        fields= "__all__"

# Formulario para details
class PhisicalExamAttendanceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
       super(PhisicalExamAttendanceForm, self).__init__(*args, **kwargs)

       self.fields['pa'].widget.attrs['readonly'] = True
       self.fields['p'].widget.attrs['readonly'] = True
       self.fields['fc'].widget.attrs['readonly'] = True
       self.fields['fr'].widget.attrs['readonly'] = True
       self.fields['tax'].widget.attrs['readonly'] = True
       self.fields['weigth'].widget.attrs['readonly'] = True
       self.fields['heigth'].widget.attrs['readonly'] = True

    class Meta:
        model = PhisicalExam
        fields= "__all__"

class PhisicalExamForm(forms.ModelForm):
    class Meta:
        model = PhisicalExam
        fields = '__all__'

class ForwardingForm(forms.ModelForm):
    class Meta:
        model = Forwarding
        fields = '__all__'