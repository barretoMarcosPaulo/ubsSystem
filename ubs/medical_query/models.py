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



class CID10(AuditModel):
    idCID10 = models.CharField('id',max_length=10, primary_key=True,unique=True)
    desc_CID10 = models.CharField('Descrição',max_length=100)
    
    def __str__(self):
        return self.desc_CID10


class ExamRequest(AuditModel):
    desc_exam = models.CharField('Descrição do exame',max_length=255)

    def __str__(self):
        return self.desc_exam



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

    # def unity_name(self):
    #     dict_unity = dict (self.unity_option)
    #     return dict_unity[self.unity]

    # def __str__(self):
    #     return self.full_name


class Query(AuditModel):
    query_type = (
        (1,'Consulta'),
        (2, 'Retorno'),
    )

    type_query = models.IntegerField('Tipo de Consulta',choices=query_type)
    main_complaint = models.TextField('Queixa Principal', max_length=400, blank=False, null=False)
    current_health_history = models.TextField('História da Doença Atual', max_length=400, blank=False, null=False)
    review_of_systems = models.TextField('Revisão de Sistemas', max_length=400, blank=False, null=False)
    epidemiological_history = models.TextField('História Epidemiológica', max_length=400, blank=False, null=False)
    previous_pathological_history = models.TextField('História Patológica Regressa', max_length=400, blank=False, null=False)
    family_history = models.TextField('História Familiar', max_length=400, blank=False, null=False)
    physiological_personal_antecedents = models.TextField('Antecedentes Pessoais Fisiológicas', max_length=400, blank=False, null=False)
    summary = models.TextField('Sumário dos Postos Principais da História e Exame Físico', max_length=400, blank=False, null=False)
    diagnostic_hypotheses = models.TextField('Hipótese(s) Diagnósticada(s)', max_length=400, blank=False, null=False)
    take_duct = models.TextField('Conduta Tomada', max_length=400, blank=False, null=False)
    PhisicalExam_idPhisicalExam = models.ForeignKey(PhisicalExam,verbose_name='Exame Físico',blank=True, null=True,on_delete=models.SET_NULL) #OBS
    Patient_idPatient = models.ForeignKey(Patient,verbose_name="Paciente", null=True, blank=True, on_delete=models.SET_NULL)
    User_idUser = models.ForeignKey(User,verbose_name="Profissional", null=True, blank=True, on_delete=models.SET_NULL)

    cid10 = models.ManyToManyField(CID10, verbose_name="CID10",related_name='cid10')
    examRequest =models.ManyToManyField(ExamRequest, verbose_name="Exame(s)",related_name='examRequest')
    medicine = models.ManyToManyField(Medicine, verbose_name="Medicamento(s)",related_name='medicine') 

    '''
    priority = models.BooleanField('Paciente Prioritário', default=False)
    opened = models.BooleanField('Consulta em Aberto', default=True)
    '''

    

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

class Query_has_Medicine(AuditModel):
    Query_idQuery = models.ForeignKey(Query,verbose_name='Consulta',null=True,on_delete=models.SET_NULL)
    Medicine_idMedicine = models.ForeignKey(Medicine,verbose_name='Medicamento', null=True,on_delete=models.SET_NULL) 
    amount = models.CharField('Quantidade',max_length=400)



# Encaminhamento do paciente, fila de espera

class Forwarding(AuditModel):
    patient= models.ForeignKey(Patient,verbose_name="Paciente", null=True, blank=True, on_delete=models.SET_NULL)
    medical = models.ForeignKey(Doctor,verbose_name="Profissional", null=True, blank=True, on_delete=models.SET_NULL)
    in_attendance = models.BooleanField('Paciente em atendimento', default=False)
    priority = models.BooleanField('Paciente Prioritário', default=False)
    
    def __str__(self):
        return self.patient.full_name

    class Meta:
        verbose_name = 'Encaminhamento'
        verbose_name_plural = 'Encaminhamentos'
        ordering = ['created_on']