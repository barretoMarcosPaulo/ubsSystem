from django.db import models
from ubs.core.models import AuditModel
from django.urls import reverse

class TypeLogradouro(AuditModel):
    desc_logradouro = models.CharField('Logradouro',max_length=45)
    
    def __str__(self):
        return self.desc_logradouro
    
    class Meta:
        verbose_name = 'Logradouro'
        verbose_name_plural = 'Logradouros'
        ordering = ['-created_on']

class State(AuditModel):
    codIBGE_UF = models.CharField("ID Estado", max_length=2, primary_key=True,unique=True)
    State_codIBGE_UF = models.CharField("Estado", max_length=50)
    UF = models.CharField("UF", max_length=2)
    region = models.CharField("Região", max_length=25)

    def __str__(self):
        return self.State_codIBGE_UF
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['-created_on']

class City(AuditModel):
    codIBGE = models.IntegerField('Código IBGE',primary_key=True,unique=True)
    codIBGE7 = models.IntegerField('Código IBGE7')
    name_city = models.CharField('Nome da cidade', max_length=45)
    port = models.CharField('Porte', max_length=20)
    capital = models.CharField('Capital', max_length=12)
    State_codIBGE_UF =  models.ForeignKey(State,verbose_name="Estado",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name_city

    def get_absolute_url(self):
        return reverse("patient:list_city")
    
    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['-created_on']

class Color(AuditModel):
    name_color = models.CharField('Cor',max_length=45)

    def __str__(self):
        return self.name_color
    
    class Meta:
        verbose_name = 'Cor'
        verbose_name_plural = 'Cores'
        ordering = ['-created_on']

class MaritalState(AuditModel):
    desc_marital_state = models.CharField('Estado Conjugal',max_length=45)

    def __str__(self):
        return self.desc_marital_state
    
    class Meta:
        verbose_name = 'Estado Conjugal'
        verbose_name_plural = 'Estados Conjugais'
        ordering = ['-created_on']

class Ocupation(AuditModel):
    desc_ocupation = models.CharField('Ocupação',max_length=60)

    def __str__(self):
        return self.desc_ocupation
    
    class Meta:
        verbose_name = 'Ocupação'
        verbose_name_plural = 'Ocupações'
        ordering = ['-created_on']

class MedicalInsurance(AuditModel):
    desc_medical_insurance = models.CharField('Convênio',max_length=13)

    def __str__(self):
        return self.desc_medical_insurance
    
    class Meta:
        verbose_name = 'Convênio'
        verbose_name_plural = 'Convênios'
        ordering = ['-created_on']


class Patient(AuditModel):
    sex_option = (
        ('M','Masculino'),
        ('F', 'Feminino'),
    )
    
    full_name = models.CharField('Nome Completo',max_length=100)
    cpf_patient = models.CharField('CPF',max_length=11,unique=True)
    sex = models.CharField('Sexo',choices=sex_option,max_length=1)
    date_birth = models.DateField('Data de Nascimento')
    local_birth = models.CharField('Local de Nascimento',max_length=60)
    Type_Logradouro_idLogradouro = models.ForeignKey(TypeLogradouro,verbose_name="Logradouro",null=True,on_delete=models.SET_NULL)                                                                                                                   
    address_name = models.CharField('Nome do Endereço',max_length=60)
    address_number = models.CharField('Número do Endereço',max_length=6,default='S/N')
    address_complement = models.CharField('Complemento do Endereço',max_length=50, null=True, blank=True)
    address_cep = models.CharField('Cep do Endereço',max_length=8,default='64600000')
    address_neighborhood = models.CharField('Bairro do Endereço',max_length=45)
    City_codIBGE = models.ForeignKey(City,verbose_name="Cidade",null=True,on_delete=models.SET_NULL)
    email = models.EmailField('email',max_length=50,null=True, blank=True)
    Color_idColor = models.ForeignKey(Color,verbose_name="Cor",null=True,on_delete=models.SET_NULL)
    Marital_State_idMarital_State = models.ForeignKey(MaritalState,verbose_name="Estado Conjugal",null=True,on_delete=models.SET_NULL)
    Ocupation_idOcupation = models.ForeignKey(Ocupation,verbose_name="Ocupação",null=True,on_delete=models.SET_NULL)
    Medical_Insurance_idMedical_insurance = models.ForeignKey(MedicalInsurance,verbose_name="Convênio",null=True,on_delete=models.SET_NULL)
    image_patient = models.ImageField(upload_to='patient/image',verbose_name="Imagem do Paciente",blank = True, null = True)
    
    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("patient:add_patient")

    def get_phone(self):
        phone = Phone.objects.filter(Patient_idPatient=self).first()
        if phone :
            return phone.phone_number
        return None

    def get_phone_type(self):
        phone = Phone.objects.filter(Patient_idPatient=self).first()
        if phone :
            return phone.phone_type
        return None
        
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_on']

    

    
class Phone(AuditModel):
    
    type_phone = (
        ('CELL','CELL'),
        ('RESIDENCIAL', 'RESIDENCIAL'),
        ('COMERCIAL', 'COMERCIAL'),
        ('FAX', 'FAX'),
    )

    phone_number = models.CharField('Número de telefone',max_length=13,unique=True)
    phone_type = models.CharField('Tipo de telefone',choices=type_phone,default='CELL',max_length=11)
    Patient_idPatient = models.ForeignKey(Patient,verbose_name="Paciente",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.phone_number
    
    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'
        ordering = ['-created_on']