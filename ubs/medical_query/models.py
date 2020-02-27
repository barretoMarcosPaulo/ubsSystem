from django.db import models
from ubs.accounts.models import User,Doctor
from ubs.core.models import AuditModel
from ubs.patient.models import Patient
from datetime import date
from django.utils import timezone
from django.urls import reverse

class PhisicalExam(AuditModel):
    
    pa = models.CharField('PA(mmHg)', max_length=45,blank=True, null=True)
    p = models.CharField('P(bpm)', max_length=45,blank=True, null=True)
    fc = models.CharField('FC(bpm)',max_length=50,blank=True, null=True)
    fr = models.CharField('FR(irpm)', max_length=45,blank=True, null=True)
    tax = models.CharField('TAX(ºC)', max_length=50, blank=True, null=True)
    weigth = models.CharField('Peso',max_length=45,blank=True, null=True)
    heigth = models.CharField('Altura(cm)',max_length=45,blank=True, null=True)

class Query(AuditModel):
    query_type = (
        (1,'Consulta'),
        (2, 'Retorno'),
    )

    type_query = models.IntegerField('Tipo de Consulta',choices=query_type)
    main_complaint = models.CharField('Queixa Principal', max_length=400, blank=False, null=False)
    current_health_history = models.CharField('História da Doença Atual', max_length=400, blank=False, null=False)
    review_of_systems = models.TextField('Revisão de Sistemas', max_length=400, blank=False, null=False)
    epidemiological_history = models.CharField('História Epidemiológica', max_length=400, blank=False, null=False)
    previous_pathological_history = models.CharField('História Patológica Regressa', max_length=400, blank=False, null=False)
    family_history = models.CharField('História Familiar', max_length=400, blank=False, null=False)
    physiological_personal_antecedents = models.CharField('Antecedentes Pessoais Fisiológicas', max_length=400, blank=False, null=False)
    summary = models.CharField('Sumário dos Postos Principais da História e Exame Físico', max_length=400, blank=False, null=False)
    diagnostic_hypotheses = models.CharField('Hipótese(s) Diagnósticada(s)', max_length=400, blank=False, null=False)
    take_duct = models.CharField('Conduta Tomada', max_length=400, blank=False, null=False)
    PhisicalExam_idPhisicalExam = models.ForeignKey(PhisicalExam,verbose_name='Exame Físico',blank=True, null=True,on_delete=models.SET_NULL) #OBS
    Patient_idPatient = models.ForeignKey(Patient,verbose_name="Paciente", null=True, blank=True, on_delete=models.SET_NULL)
    User_idUser = models.ForeignKey(User,verbose_name="Profissional", null=True, blank=True, on_delete=models.SET_NULL)

    '''
    priority = models.BooleanField('Paciente Prioritário', default=False)
    opened = models.BooleanField('Consulta em Aberto', default=True)
    '''

    def __int__(self):
        return self.patient
    
    def __str__(self):
        return self.Patient_idPatient

    def get_absolute_url(self):
        return reverse('medical_query:list_query')

    def get_physical_exam(self):
        return PhisicalExam.objects.filter(id=self.PhisicalExam_idPhisicalExam.id).first()
    
    def get_type_query(self):
        query_type = {
            1:'Consulta',
            2:'Retorno'
        }
        return Query.query_type[self.type_query][1]

    class Meta:
        verbose_name = 'Consulta Medica'
        verbose_name_plural = 'Consultas Medicas'
        ordering = ['created_on']


    
class CID10(AuditModel):
    idCID10 = models.CharField('id',max_length=10, primary_key=True,unique=True)
    desc_CID10 = models.CharField('Descrição',max_length=100)
    
    def __str__(self):
        return self.desc_CID10

class QueryHasCID10(AuditModel):
    Query_idQuery_CID = models.ForeignKey(Query,verbose_name='Id da consulta',null=True,blank=True,on_delete=models.SET_NULL) 
    CID10_idCID10 = models.ForeignKey(CID10,verbose_name='CID 10',null=True,blank=True,on_delete=models.SET_NULL)

class ExamRequest(AuditModel):
    desc_exam = models.CharField('Descrição do exame',max_length=255)

class QueryHasExamRequest(AuditModel):
    Query_idQuery_EXAM = models.ForeignKey(Query,verbose_name='Requisição de exame',null=True,blank=True,on_delete=models.SET_NULL)
    ExamRequest_idExam = models.ForeignKey(ExamRequest,verbose_name='Exame',null=True,blank=True,on_delete=models.SET_NULL)

class Medicine(AuditModel):
    unity_option = (
        ('CX','Caixa'),
        ('VD', 'Vidro'),
        ('FR', 'Frasco'),
        ('AM', 'Ampola'),
        ('CO', 'Comprimido'),
    )

    full_name = models.CharField('Nome do remedio',max_length=100)
    generic_name = models.CharField('Nome generico',max_length=100)
    dosage = models.CharField('Dosagem',max_length=255)
    unity = models.CharField('Unidade',choices=unity_option,max_length=3)

class QueryHasMedicine(AuditModel):
    amount = models.IntegerField('Quantidade')
    Query_idQuery_MEDICINE = models.ForeignKey(Query,verbose_name='Id da consulta',null=True,blank=True,on_delete=models.SET_NULL)
    Medicine_idMedicine = models.ForeignKey(Medicine,verbose_name='Id do remédio',null=True,blank=True,on_delete=models.SET_NULL)



# Encaminhamento do paciente, fila de espera

class Forwarding(AuditModel):
    patient= models.ForeignKey(Patient,verbose_name="Paciente", null=True, blank=True, on_delete=models.SET_NULL)
    medical = models.ForeignKey(Doctor,verbose_name="Profissional", null=True, blank=True, on_delete=models.SET_NULL)
    in_attendance = models.BooleanField('Paciente em atendimento', default=False)

    def __str__(self):
        return self.patient.full_name

    class Meta:
        verbose_name = 'Encaminhamento'
        verbose_name_plural = 'Encaminhamentos'
        ordering = ['created_on']