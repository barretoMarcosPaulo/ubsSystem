import re
import uuid
from django.db import models
from django.urls import reverse
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from ubs.core.models import AuditModel

class User(AbstractBaseUser, PermissionsMixin):
    # user_type_option = (
    #     ('1','Admin'),
    #     ('2', 'Médico(a)'),
    #     ('3', 'Atendente'),
    # )
    # user_status = (
    #     ('1','Ativo'),
    #     ('2','Inativo'),
    # )

    username = models.CharField(
        'Usuário', max_length=200, default=uuid.uuid4, unique=True, validators=[
        validators.RegexValidator(
            re.compile('^[\w.@+-]+$'),
            'Informe um nome de usuário válido. '
            'Este valor deve conter apenas letras, números '
            'e os caracteres: @/./+/-/_ .'
            , 'invalid'
        )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    full_name = models.CharField('Nome Completo',max_length=100)
    cpf = models.CharField('CPF', max_length=11)
    phone = models.CharField('Telefone', max_length=13)
    email = models.EmailField('Email',max_length=100)
    # type_user = models.IntegerField('Tipo de usuário',choices=user_type_option, null=True, blank=True)
    # status = models.IntegerField('Status do usuário',choices=user_status,null=True, blank=True)
    # image = models.CharField('Imagem', max_length=255)
    is_staff = models.BooleanField('is staff',default=False)
    is_clerk = models.BooleanField('Atendente',default=False)
    is_doctor = models.BooleanField('Medico',default=False)

    def __str__(self):
        return self.full_name
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_absolute_url(self):
        return reverse('accounts:list_all_admin')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    



class Clerk(User):
    register_clerk = models.CharField('registro do atendente', max_length=12)

    def get_absolute_url(self):
        return reverse('accounts:list_all_clerk')  


class Doctor(User):
    crm_doc = models.CharField('CRM do médico', max_length=20)
    
    def get_absolute_url(self):
        return reverse('accounts:list_all_doctor')  



class MedicalSpecialty(AuditModel):
    desc_specialty = models.CharField('Descrição especialidade(s)',max_length=100)



class DoctorHasMedicalSpecialty(Doctor):
    MedicalSpecialty_idSpecialty = models.ForeignKey(MedicalSpecialty,verbose_name='Especialidade',null=True,blank=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'
