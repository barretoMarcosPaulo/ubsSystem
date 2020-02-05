from django.urls import path 
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.ListPatient.as_view(), name='list_patient'),
    path('adicionar', views.PatientCreate.as_view(), name='add_patient'),
    path('editar/<int:pk> ', views.PatientUpdate.as_view(), name='update_patient'),
    path('detalhes/<int:pk> ', views.PatientDetail.as_view(), name='detail_patient'),

]