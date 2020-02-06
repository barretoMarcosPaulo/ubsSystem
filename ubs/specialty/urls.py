from django.urls import path 
from . import views

app_name = 'specialty'

urlpatterns = [
    path('add', views.SpecialtyCreate.as_view(),name='add_specialty' ),
    path('list', views.SpecialtyList.as_view(),name='list_specialty' ),
    path('edit/<int:pk>', views.SpecialtyUpdate.as_view(),name='edit_specialty' ),
    path('delete/<int:pk>', views.SpecialtyDelete.as_view(),name='delete_specialty' ),

    path('add/vinculo', views.DoctorSpecialtyCreate.as_view(),name='add_doctor_specialty' ),
    path('list/vinculos', views.DoctorSpecialtyList.as_view(),name='list_doctor_specialty' ),
    path('edit/vinculo/<int:pk>', views.DoctorSpecialtyUpdate.as_view(),name='edit_doctor_specialty' ),
    path('delete/vinculo/<int:pk>', views.DoctorSpecialtyDelete.as_view(),name='delete_sdoctor_pecialty' ),
]