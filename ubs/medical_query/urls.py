from django.urls import path 
from . import views
from .models import ExamRequest

app_name = 'medical_query'

urlpatterns = [
    path('consultar/<int:patient_pk>/<int:forwarding_pk>', views.QueryCreate.as_view(), name='add_query'),
    path('consulta-historico/list', views.ListQuerysHistory.as_view(), name='list_query_history'),
    path('consulta/edit/<int:pk> ', views.QueryUpdate.as_view(), name='update_query'),
    path('consulta/detalhes/<int:pk> ', views.Attendances.as_view(), name='detail_query'),
    path('atendimentos/list', views.ListAttendances.as_view(), name='list_attendances'),    

    path('encaminhamento/', views.ForwardingCreate.as_view(), name='forwarding_create'),    
    path('encaminhamentos-realizados/', views.ForwardingList.as_view(), name='all_forwarding'),
    path('encaminhamentos-dia/', views.CurrentForwardingList.as_view(), name='currents_forwarding'),

    path('atendimentos-dia/', views.AwaitQuerys.as_view(), name='await_querys'),  
    
    # Para o Técnico
    path('fila-de-espera/', views.AwaitQuerysClerk.as_view(), name='await_querys_clerk'),  

    path('adicionar-CID', views.CID10Create.as_view(),name="add_CID"),
    path('listagem-CID', views.ListCID10.as_view(),name="list_CID"),
    path('detalhes-CID/<str:pk> ', views.CID10Detail.as_view(), name='detail_CID'),
    path('editar-CID/<str:pk> ', views.CID10Update.as_view(), name='update_CID'),
    path('delete-CID/<str:pk>', views.DeleteCID10.as_view(), name='delete_CID'),

    path('adicionar-medicamento', views.MedicineCreate.as_view(),name="add_medicine"),
    path('listagem-medicamento', views.ListMedicine.as_view(),name="list_medicine"),
    path('detalhes-medicamento/<str:pk> ', views.MedicineDetail.as_view(), name='detail_medicine'),
    path('editar-medicamento/<str:pk> ', views.MedicineUpdate.as_view(), name='update_medicine'),
    path('delete-medicamento/<str:pk>', views.DeleteMedicine.as_view(), name='delete_medicine'),
    
    path('adicionar-requisicao-exame', views.ExamRequestCreate.as_view(),name="add_exam_request"),
    path('listagem-requisicao-exame', views.ListExamRequest.as_view(),name="list_exam_request"),
    path('editar-requisicao-exame/<str:pk> ', views.ExamRequestUpdate.as_view(), name='update_exam_request'),
    path('detalhes-requisicao-exame/<str:pk> ', views.ExamRequestDetail.as_view(), name='detail_exam_request'),
    path('delete-requisicao-exame/<str:pk>', views.DeleteExamRequest.as_view(), name='delete_exam_request'),
    
    path('receita/<int:query_pk>', views.Recipe.as_view(), name='recipe'),
    path('exames/<int:query_pk>', views.ExamRequestPDF.as_view(), name='exam_request_pdf'),

    path('exames/autocomplete', views.ExamRequestAutocomplete.as_view(create_field='desc_exam',model=ExamRequest), name='examRequest_autocomplete'),
    path('cid10/autocomplete', views.CID10Autocomplete.as_view(), name='cid10_autocomplete'),
    path('medicine/autocomplete', views.MedicineAutocomplete.as_view(), name='medicine_autocomplete'),
]