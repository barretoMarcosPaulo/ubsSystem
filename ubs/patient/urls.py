from django.urls import path 
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.ListPatient.as_view(), name='list_patient'),
    path('adicionar-paciente', views.PatientCreate.as_view(), name='add_patient'),
    path('editar-paciente/<int:pk> ', views.PatientUpdate.as_view(), name='update_patient'),
    path('detalhes-paciente/<int:pk> ', views.PatientDetail.as_view(), name='detail_patient'),
    path('delete-paciente/<int:pk>', views.DeletePatient.as_view(), name='delete_patient'),

    path('adicionar-cidade', views.CityCreate.as_view(),name="add_city"),
    path('detalhes-cidades/<int:pk> ', views.CityDetail.as_view(), name='detail_city'),
    path('editar-cidade/<int:pk> ', views.CityUpdate.as_view(), name='update_city'),
    path('listagem-cidade', views.ListCity.as_view(),name="list_city"),
    path('delete-cidade/<int:pk>', views.DeleteCity.as_view(), name='delete_city'),

]