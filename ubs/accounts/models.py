import re
import uuid
from django.db import models
from django.urls import reverse
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


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
  name = models.CharField('Nome', max_length=150)
  cpf = models.CharField('CPF', max_length=14)
  email = models.EmailField('E-mail', unique=True, max_length=255)
  is_Medical= models.BooleanField('Médico', default=False)
  is_Triagem = models.BooleanField('Triagem', default=True)
  is_superuser = models.BooleanField('Super Usuário', default=False)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  class Meta:
    verbose_name = 'Usuário'
    verbose_name_plural = 'Usuários'

