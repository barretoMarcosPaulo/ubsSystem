from django.contrib import admin

# Register your models here.
from .models import Patient
from .models import MedicalQuery

admin.site.register(Patient)
admin.site.register(MedicalQuery)