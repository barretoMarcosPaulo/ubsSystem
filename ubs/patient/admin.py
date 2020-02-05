from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(TypeLogradouro)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Color)
admin.site.register(MaritalState)
admin.site.register(Ocupation)
admin.site.register(MedicalInsurance)
admin.site.register(Phone)