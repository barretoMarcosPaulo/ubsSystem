from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    # URLS for admin views
    path('admin/add', views.AdminCreate.as_view(), name='add_admin'),
    
    
    # URLS for clerks views
    path('clerk/add', views.ClerkCreate.as_view(), name='add_clerk'),
    # path('list', views.ListPatient.as_view(), name='list_patient'),
    # path('edit/<int:pk> ', views.PatientUpdate.as_view(), name='update_patient'),
    # path('delete/<int:id> ', views.delete_patient, name='delete_patient'),
    # path('detalhes/<int:pk> ', views.PatientDetail.as_view(), name='detail_patient'),

]