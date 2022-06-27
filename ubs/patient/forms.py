from dal import autocomplete
from django import forms
from django.forms import inlineformset_factory

from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            "Type_Logradouro_idLogradouro": autocomplete.ModelSelect2(
                url="patient:logradouro_autocomplete", attrs={"class": "col-md-10"}
            ),
            "City_codIBGE": autocomplete.ModelSelect2(url="patient:city_autocomplete", attrs={"class": "col-md-10"}),
            "Medical_Insurance_idMedical_insurance": autocomplete.ModelSelect2(
                url="patient:medicalInsurance_autocomplete", attrs={"class": "col-md-10"}
            ),
            "Color_idColor": autocomplete.ModelSelect2(url="patient:color_autocomplete", attrs={"class": "col-md-10"}),
            "Marital_State_idMarital_State": autocomplete.ModelSelect2(
                url="patient:maritalState_autocomplete", attrs={"class": "col-md-10"}
            ),
            "Ocupation_idOcupation": autocomplete.ModelSelect2(url="patient:ocupation_autocomplete", attrs={"class": "col-md-10"}),
        }


class PatientDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = Patient
        fields = "__all__"


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"


class CityEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CityEditForm, self).__init__(*args, **kwargs)
        self.fields["codIBGE"].widget.attrs["readonly"] = True

    class Meta:
        model = City
        fields = "__all__"


class CityDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CityDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = City
        fields = "__all__"


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = "__all__"


class StateEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StateEditForm, self).__init__(*args, **kwargs)
        self.fields["codIBGE_UF"].widget.attrs["readonly"] = True

    class Meta:
        model = State
        fields = "__all__"


class StateDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StateDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = State
        fields = "__all__"


class MedicalInsuranceForm(forms.ModelForm):
    class Meta:
        model = MedicalInsurance
        fields = "__all__"


class MedicalInsuranceDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicalInsuranceDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = MedicalInsurance
        fields = "__all__"


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"


class ColorDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColorDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = Color
        fields = "__all__"


class MaritalStateForm(forms.ModelForm):
    class Meta:
        model = MaritalState
        fields = "__all__"


class MaritalStateDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaritalStateDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = MaritalState
        fields = "__all__"


class TypeLogradouroForm(forms.ModelForm):
    class Meta:
        model = TypeLogradouro
        fields = "__all__"


class TypeLogradouroDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TypeLogradouroDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = TypeLogradouro
        fields = "__all__"


class OcupationForm(forms.ModelForm):
    class Meta:
        model = Ocupation
        fields = "__all__"


class OcupationDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OcupationDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True

    class Meta:
        model = Ocupation
        fields = "__all__"
