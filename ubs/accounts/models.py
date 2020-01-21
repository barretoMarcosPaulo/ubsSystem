import re
import uuid
from easy_thumbnails.fields import ThumbnailerImageField
from django.db import models
from django.urls import reverse
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from datetime import date
from chainforeducation.nucleo.models import *
from chainforeducation.ensino.models import *


class AuditModel(models.Model):
	# Audit Fields
	created_on = models.DateTimeField('Criado em', auto_now_add=True)
	updated_on = models.DateTimeField('Autalizado em', auto_now=True)

	class Meta:
		abstract=True


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
	rg = models.CharField('RG', max_length=14)
	matricula = models.CharField('Matricula', max_length=100, blank=False, null=False)
	email = models.EmailField('E-mail', unique=True, max_length=255)
	is_staff = models.BooleanField('Equipe', default=False)
	is_active = models.BooleanField('Ativo', default=True)
	is_superuser = models.BooleanField('Super Usuário', default=False)
	date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
	birth_date = models.DateField('Data de Nascimento', blank=True, null=True)
	MALE = 'M'
	FEMALE = 'F'
	SEX_CHOICES = ((MALE, 'Masculino'), (FEMALE, 'Feminino'),)
	sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES, default=FEMALE)
	MARRIED = 'CASADO'
	SINGLE = 'SOLTEIRO'
	SEPARATED = 'SEPARADO'
	WINDOWER = 'VIUVO'
	DIVORCED = 'DIVORCIADO'
	MARITAL_STATUS_CHOICES = ((MARRIED, 'Casado'), (SINGLE, 'Solteiro'), (SEPARATED, 'Separado'), (WINDOWER, 'Viúvo'), (DIVORCED, 'Divorciado'),)
	marital_status = models.CharField('Estado Cívil', max_length=10, choices=MARITAL_STATUS_CHOICES, default=SINGLE)
	phone = models.CharField('Telefone', blank=True, max_length=17)
	avatar = ThumbnailerImageField(
		upload_to="avatar",
		blank=True,
		resize_source=dict(size=(215, 215), crop=True)
	)

	address = GenericRelation('Address')

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	""" Método deletar a imagem (avatar) quando alterada ou excluida """
	def delete(self):
		self.avatar.delete()
		return super(User, self).delete()


	def __str__(self):
		return self.first_name or self.username

	def get_full_name(self):
		return ('%s  %s') % (self.first_name, self.last_name)

	def get_short_name(self):
		return str(self).split(" ")[0]

	class Meta:
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'
