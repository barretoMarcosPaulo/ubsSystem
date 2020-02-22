from django.urls import path 
from . import views

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # URLS for admin views
    path('admin/add', views.AdminCreate.as_view(), name='add_admin'),
    path('admin/list/all', views.AdminList.as_view(), name='list_all_admin'),
    path('admin/edit/<int:pk>', views.AdminUpdate.as_view(), name='update_admin'),
    path('admin/delete/<int:pk>', views.AdminDelete.as_view(), name='delete_admin'),
    
    
    # URLS for clerks views
    path('clerk/add', views.ClerkCreate.as_view(), name='add_clerk'),
    path('clerk/list/all', views.ClerkList.as_view(), name='list_all_clerk'),
    path('clerk/edit/<int:pk>', views.ClerkUpdate.as_view(), name='update_clerk'),
    path('clerk/delete/<int:pk>', views.ClerkDelete.as_view(), name='delete_clerk'),

    #URLS for doctor view
    path('doctor/add', views.DoctorCreate.as_view(), name='add_doctor'),
    path('doctor/list/all', views.DoctorList.as_view(), name='list_all_doctor'),
    path('doctor/edit/<int:pk>', views.DoctorUpdate.as_view(), name='update_doctor'),
    path('doctor/delete/<int:pk>', views.DoctorDelete.as_view(), name='delete_doctor'),

    path(
        'login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True, 
        redirect_field_name='/core/'
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/'
        ),
        name='logout'
    ),


    # path('list', views.ListPatient.as_view(), name='list_patient'),
    # path('edit/<int:pk> ', views.PatientUpdate.as_view(), name='update_patient'),
    # path('delete/<int:id> ', views.delete_patient, name='delete_patient'),
    # path('detalhes/<int:pk> ', views.PatientDetail.as_view(), name='detail_patient'),

]