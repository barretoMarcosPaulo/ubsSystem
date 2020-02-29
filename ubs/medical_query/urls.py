from django.urls import path 
from . import views

app_name = 'medical_query'

urlpatterns = [
    path('consultar/<int:patient_pk>/<int:forwarding_pk>', views.QueryCreate.as_view(), name='add_query'),
    path('consulta-historico/list', views.ListQuerysHistory.as_view(), name='list_query_history'),
    path('consulta/edit/<int:pk> ', views.QueryUpdate.as_view(), name='update_query'),
    path('consulta/detalhes/<int:pk> ', views.Attendances.as_view(), name='detail_query'),
    path('atendimentos/list', views.ListAttendances.as_view(), name='list_attendances'),    

    path('encaminhamento/', views.ForwardingCreate.as_view(), name='forwarding_create'),    
    path('encaminhamentos-realizados/', views.ForwardingList.as_view(), name='currents_forwarding'),

    path('atendimentos-dia/', views.AwaitQuerys.as_view(), name='await_querys'),  

    path('adicionar-CID', views.CID10Create.as_view(),name="add_CID"),
    path('listagem-CID', views.ListCID10.as_view(),name="list_CID"),
    
]