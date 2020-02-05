from django import forms
from django.contrib.auth import get_user_model
from dal import autocomplete
from .models import *


class SpecialtyForm(forms.ModelForm):
    
	class Meta:
		model = MedicalSpecialty
		fields = "__all__"


class DoctorSpecialtyForm(forms.ModelForm):
    
	class Meta:
		model = DoctorHasMedicalSpecialty
		fields = ['doctor','MedicalSpecialty_idSpecialty']

		# widgets = {
        #     'doctor': autocomplete.ModelSelect2Multiple(url='atendimento:membros_autocomplete'),
        # }