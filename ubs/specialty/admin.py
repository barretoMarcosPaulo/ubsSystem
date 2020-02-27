from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources,fields

admin.site.register(DoctorHasMedicalSpecialty)

class MedicalSpecialtyResource(resources.ModelResource):
    class Meta:
        model = MedicalSpecialty
        import_id_fields = ('desc_specialty',)
        exclude = ('id','created_on', 'updated_on')

@admin.register(MedicalSpecialty)
class MedicalSpecialtyResource(ImportExportModelAdmin):
    resource_class = MedicalSpecialtyResource