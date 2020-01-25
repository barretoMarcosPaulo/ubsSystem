from django.urls import path 
from . import views

app_name = 'medical_query'

urlpatterns = [
    path('paciente/add', views.new_patient, name='add_patient'),
    path('paciente/list', views.ListPatient.as_view(), name='list_patient'),
    path('paciente/edit/<int:pk> ', views.PatientUpdate.as_view(), name='update_patient'),
    path('paciente/delete/<int:id> ', views.delete_patient, name='delete_patient'),

    path('consulta/add', views.QueryCreate.as_view(), name='add_query'),
]