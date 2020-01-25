from django.urls import path 
from . import views

app_name = 'medical_query'

urlpatterns = [
    path('paciente/add', views.new_patient, name='add_patient'),

    path('consulta/add', views.QueryCreate.as_view(), name='add_query'),
]