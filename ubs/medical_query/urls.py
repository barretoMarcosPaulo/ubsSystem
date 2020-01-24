from django.urls import path 
from . import views

app_name = 'medical_query'

urlpatterns = [
    path('', views.new_patient, name='patient'),
]