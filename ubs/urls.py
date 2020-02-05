from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('ubs.core.urls')),
    path('medical_query/', include('ubs.medical_query.urls')),
    path('paciente/', include('ubs.patient.urls')),
    path('accounts/', include('ubs.accounts.urls')),
    path('specialty/', include('ubs.specialty.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
