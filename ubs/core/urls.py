from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(),name="index"),
    path('dashboard', DashboardView.as_view(),name="dashboard"),
    path('dashboard/adicionar', PatientCreate.as_view(),name="add_patient"),
    path('dashboard/listagem-paciente', ListPatient.as_view(),name="list_patient"),
    path('dashboard/delete-paciente/<int:pk>', DeleteProposal.as_view(), name='delete_patient'),
    path('dashboard/editar-paciente/<int:pk> ', PatientUpdate.as_view(), name='update_patient'),
    path('dashboard/detalhes-paciente/<int:pk> ', PatientDetail.as_view(), name='detail_patient'),

    
]