import re
import uuid
from django.db import models
from django.urls import reverse
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

'''class User(AbstractBaseUser, PermissionsMixin): 

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
  name = models.CharField('Nome', max_length=150)
  cpf = models.CharField('CPF', max_length=14)
  email = models.EmailField('E-mail', unique=True, max_length=255)
  is_Medical= models.BooleanField('Médico', default=False)
  is_Triagem = models.BooleanField('Triagem', default=True)
  is_superuser = models.BooleanField('Super Usuário', default=False)
  is_staff = models.BooleanField('Equipe', default=False)
  is_active = models.BooleanField('Ativo', default=True)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  class Meta:
    verbose_name = 'Usuário'
    verbose_name_plural = 'Usuários'

'''

class User(AbstractBaseUser, PermissionsMixin): 

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
    password = models.CharField('Senha', max_length=255)
    type_user = models.IntegerField('Tipo de usuário')
    status = models.IntegerField('Status do usuário')
    image = models.CharField('Imagem', max_length=255)

    def __str__(self):
        return self.full_name
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
class Clerk(User):
    register_clerk = models.CharField('registro do atendente', max_length=12)

class Doctor(User):
    CRM_doc = models.CharField('CRM do médico', max_length=20)
    
class MedicalSpecialty():
    desc_specialty = models.CharField('Descrição especialidade(s)', max_length=100)

class DoctorHasMedicalSpecialty(Doctor):
    MedicalSpecialty_idSpecialty = models.ForeignKey(MedicalSpecialty,verbose_name='Especialidade',null=True,blank=True,on_delete=models.SET_NULL)
