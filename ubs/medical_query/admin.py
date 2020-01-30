from django.contrib import admin

# Register your models here.
from .models import MedicalQuery

admin.site.register(MedicalQuery)