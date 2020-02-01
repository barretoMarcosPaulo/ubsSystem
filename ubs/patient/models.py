from django.db import models
from ubs.core.models import AuditModel
from django.urls import reverse

class TypeLogradouro(AuditModel):
    desc_logradouro = models.CharField('Logradouro',max_length=45)

class State(AuditModel):
    State_codIBGE_UF = models.CharField("Estado", max_length=50)
    UF = models.CharField("UF", max_length=2)
    region = models.CharField("Região", max_length=25)

class City(AuditModel):
    codIBGE7 = models.IntegerField('Código IBGE',primary_key=True,unique=True)
    codIBGE7 = models.IntegerField('Código IBGE7')
    name_city = models.CharField('Nome da cidade', max_length=45)
    port = models.CharField('Porta', max_length=20)
    capital = models.CharField('Capital', max_length=12)
    state =  models.ForeignKey(State,verbose_name="Estado",null=True,blank=True,on_delete=models.SET_NULL)

class Color(AuditModel):
    name_color = models.CharField('Cor',max_length=45)

class MaritalState(AuditModel):
    desc_marital_state = models.CharField('Estado Conjugal',max_length=45)

class Ocupation(AuditModel):
    desc_ocupation = models.CharField('Ocupação',max_length=60)

class MedicalInsurance(AuditModel):
    desc_medical_insurance = models.CharField('Convênio',max_length=13)



class Patient(AuditModel):
    sex_option = (
        ('M','Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )

    full_name = models.CharField('Nome Completo',max_length=100)
    cpf_patient = models.CharField('cpf',max_length=100)
    sex = models.CharField('Sexo',choices=sex_option,max_length=1)
    date_birth = models.DateField('Data de Nascimento')
    local_birth = models.CharField('Local de Nascimento',max_length=60)
    Type_Logradouro_idLogradouro = models.ForeignKey(TypeLogradouro,verbose_name="Logradouro",null=True,blank=True,on_delete=models.SET_NULL)                                                                                                                   
    address_name = models.CharField('Nome do Endereço',max_length=60)
    address_numero = models.CharField('Número do Endereço',max_length=6)
    address_complement = models.CharField('Complemento do Endereço',max_length=50, null=True, blank=True)
    address_cep = models.CharField('cep do Endereço',max_length=8)
    address_neighborhood = models.CharField('Vizinhança do Endereço',max_length=45)
    City_codIBGE = models.ForeignKey(City,verbose_name="Cidade",null=True,blank=True,on_delete=models.SET_NULL)
    email = models.EmailField('email',max_length=50,null=True, blank=True)
    image_patient = models.ImageField(upload_to='patient',blank = True, null = True)
    Color_idColor = models.ForeignKey(Color,verbose_name="Cor",null=True,blank=True,on_delete=models.SET_NULL)
    Marital_State_idMarital_State = models.ForeignKey(MaritalState,verbose_name="Estado Conjugal",null=True,blank=True,on_delete=models.SET_NULL)
    Ocupation_idOcupation = models.ForeignKey(Ocupation,verbose_name="Ocupação",null=True,blank=True,on_delete=models.SET_NULL)
    Medical_Insurance_idMedical_insurance = models.ForeignKey(MedicalInsurance,verbose_name="Convênio",null=True,blank=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("patient:register_patient")


    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_on']

    

    
class Phone(AuditModel):
    phone_number = models.CharField('Número de telefone',max_length=13,unique=True)
    phone_type = models.CharField('Tipo de telefone',max_length=11)
    Patient_idPatient = models.ForeignKey(Patient,verbose_name="Telefone",null=True,blank=True,on_delete=models.SET_NULL)
