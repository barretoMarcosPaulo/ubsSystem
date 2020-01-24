from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ubs.core.urls')),
    path('medical_query/', include('ubs.medical_query.urls')),
]
