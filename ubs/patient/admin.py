from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget

admin.site.register(Patient)
# admin.site.register(Color)
# admin.site.register(MaritalState)
# admin.site.register(MedicalInsurance)
# admin.site.register(TypeLogradouro)
# admin.site.register(State)
# admin.site.register(City)
# admin.site.register(Ocupation)

class TypeLogradouroResource(resources.ModelResource):
    class Meta:
        model = TypeLogradouro
        import_id_fields = ('desc_logradouro',)
        exclude = ('id','created_on', 'updated_on')

@admin.register(TypeLogradouro)
class TypeLogradouroResource(ImportExportModelAdmin):
    resource_class = TypeLogradouroResource

class ColorResource(resources.ModelResource):
    class Meta:
        model = Color
        import_id_fields = ('name_color',)
        exclude = ('id','created_on', 'updated_on')

@admin.register(Color)
class ColorResource(ImportExportModelAdmin):
    resource_class = ColorResource

class MaritalStateResource(resources.ModelResource):
    class Meta:
        model = MaritalState
        import_id_fields = ('desc_marital_state',)
        exclude = ('id','created_on', 'updated_on')

@admin.register(MaritalState)
class MaritalStateResource(ImportExportModelAdmin):
    resource_class = MaritalStateResource

class MedicalInsuranceResource(resources.ModelResource):
    class Meta:
        model = MedicalInsurance
        import_id_fields = ('desc_medical_insurance',)
        exclude = ('id','created_on', 'updated_on')

@admin.register(MedicalInsurance)
class MedicalInsuranceResource(ImportExportModelAdmin):
    resource_class = MedicalInsuranceResource

class OcupationResource(resources.ModelResource):
    class Meta:
        model = Ocupation
        exclude = ('created_on', 'updated_on')

@admin.register(Ocupation)
class OcupationResource(ImportExportModelAdmin):
    resource_class = OcupationResource

class CityResource(resources.ModelResource):
    State_codIBGE_UF = fields.Field(
        column_name='State_codIBGE_UF',
        attribute='State_codIBGE_UF',
        widget=ForeignKeyWidget(State, 'UF'))
    class Meta:
        import_id_fields = ('codIBGE',)
        model = City
        exclude = ('created_on', 'updated_on')
        export_order = ['codIBGE', 'codIBGE7','State_codIBGE_UF','name_city','port','capital']

@admin.register(City)
class CityResource(ImportExportModelAdmin):
    resource_class = CityResource

class SatateResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codIBGE_UF',)
        model = State
        exclude = ('created_on', 'updated_on')

@admin.register(State)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = SatateResource

