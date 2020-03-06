from django.urls import path 
from . import views

app_name = 'patient'

urlpatterns = [
    path('listagem-paciente', views.ListPatient.as_view(), name='list_patient'),
    path('adicionar-paciente', views.PatientCreate.as_view(), name='add_patient'),
    path('editar-paciente/<int:pk> ', views.PatientUpdate.as_view(), name='update_patient'),
    path('detalhes-paciente/<int:pk> ', views.PatientDetail.as_view(), name='detail_patient'),
    path('delete-paciente/<int:pk>', views.DeletePatient.as_view(), name='delete_patient'),

    path('adicionar-cidade', views.CityCreate.as_view(),name="add_city"),
    path('detalhes-cidades/<int:pk> ', views.CityDetail.as_view(), name='detail_city'),
    path('editar-cidade/<int:pk> ', views.CityUpdate.as_view(), name='update_city'),
    path('listagem-cidade', views.ListCity.as_view(),name="list_city"),
    path('delete-cidade/<int:pk>', views.DeleteCity.as_view(), name='delete_city'),

    path('adicionar-estado', views.StateCreate.as_view(),name="add_state"),
    path('listagem-estado', views.ListState.as_view(),name="list_state"),
    path('detalhes-estado/<str:pk> ', views.StateDetail.as_view(), name='detail_state'),
    path('editar-estado/<str:pk> ', views.StateUpdate.as_view(), name='update_state'),
    path('delete-estado/<str:pk>', views.DeleteState.as_view(), name='delete_state'),
   
    path('adicionar-convenio', views.MedicalInsuranceCreate.as_view(),name="add_medical_insurance"),
    path('listagem-convenio', views.ListMedicalInsurance.as_view(),name="list_medical_insurance"),
    path('detalhes-convenio/<int:pk> ', views.MedicalInsuranceDetail.as_view(), name='detail_medical_insurance'),
    path('editar-convenio/<int:pk> ', views.MedicalInsuranceUpdate.as_view(), name='update_medical_insurance'),
    path('delete-convenio/<int:pk>', views.DeleteMedicalInsurance.as_view(), name='delete_medical_insurance'),
    
    path('adicionar-cor', views.ColorCreate.as_view(),name="add_color"),
    path('listagem-cor', views.ListColor.as_view(),name="list_color"),
    path('detalhes-cor/<int:pk> ', views.ColorDetail.as_view(), name='detail_color'),
    path('editar-cor/<int:pk> ', views.ColorUpdate.as_view(), name='update_color'),
    path('delete-cor/<int:pk>', views.DeleteColor.as_view(), name='delete_color'),

    path('adicionar-estado-conjugal', views.MaritalStateCreate.as_view(),name="add_marital_state"),
    path('listagem-estado-conjugal', views.ListMaritalState.as_view(),name="list_marital_state"),
    path('detalhes-estado-conjugal/<int:pk> ', views.MaritalStateDetail.as_view(), name='detail_marital_state'),
    path('editar-estado-conjugal/<int:pk> ', views.MaritalStateUpdate.as_view(), name='update_marital_state'),
    path('delete-estado-conjugal/<int:pk>', views.DeleteMaritalState.as_view(), name='delete_marital_state'),

    path('adicionar-logradouro', views.TypeLogradouroCreate.as_view(),name="add_logradouro"),
    path('listagem-logradouro', views.ListTypeLogradouro.as_view(),name="list_logradouro"),
    path('detalhes-logradouro/<int:pk> ', views.TypeLogradouroDetail.as_view(), name='detail_logradouro'),
    path('editar-logradouro/<int:pk> ', views.TypeLogradouroUpdate.as_view(), name='update_logradouro'),
    path('delete-logradouro/<int:pk>', views.DeleteTypeLogradouro.as_view(), name='delete_logradouro'),
    
    path('adicionar-ocupacao', views.OcupationCreate.as_view(),name="add_ocupation"),
    path('listagem-ocupacao', views.ListOcupation.as_view(),name="list_ocupation"),
    path('detalhes-ocupacao/<int:pk> ', views.OcupationDetail.as_view(), name='detail_ocupation'),
    path('editar-ocupacao/<int:pk> ', views.OcupationUpdate.as_view(), name='update_ocupation'),
    path('delete-ocupacao/<int:pk>', views.DeleteOcupation.as_view(), name='delete_ocupation'),
   
    path('logradouro-autocomplete', views.TypeLogradouroAutocomplete.as_view(),name="logradouro_autocomplete"),

]