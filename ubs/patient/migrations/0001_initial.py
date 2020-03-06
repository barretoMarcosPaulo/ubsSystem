# Generated by Django 2.2.6 on 2020-03-06 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('codIBGE', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Código IBGE')),
                ('codIBGE7', models.IntegerField(verbose_name='Código IBGE7')),
                ('name_city', models.CharField(max_length=45, verbose_name='Nome da cidade')),
                ('port', models.CharField(max_length=20, verbose_name='Porte')),
                ('capital', models.CharField(default='N', max_length=12, verbose_name='Capital')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('name_color', models.CharField(max_length=45, verbose_name='Cor')),
            ],
            options={
                'verbose_name': 'Cor',
                'verbose_name_plural': 'Cores',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='MaritalState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_marital_state', models.CharField(max_length=45, verbose_name='Estado Conjugal')),
            ],
            options={
                'verbose_name': 'Estado Conjugal',
                'verbose_name_plural': 'Estados Conjugais',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='MedicalInsurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_medical_insurance', models.CharField(max_length=13, verbose_name='Convênio')),
            ],
            options={
                'verbose_name': 'Convênio',
                'verbose_name_plural': 'Convênios',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Ocupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_ocupation', models.CharField(max_length=60, verbose_name='Ocupação')),
            ],
            options={
                'verbose_name': 'Ocupação',
                'verbose_name_plural': 'Ocupações',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('codIBGE_UF', models.CharField(max_length=2, primary_key=True, serialize=False, unique=True, verbose_name='ID Estado')),
                ('State_codIBGE_UF', models.CharField(max_length=50, verbose_name='Estado')),
                ('UF', models.CharField(max_length=2, verbose_name='UF')),
                ('region', models.CharField(max_length=25, verbose_name='Região')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='TypeLogradouro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_logradouro', models.CharField(max_length=45, verbose_name='Logradouro')),
            ],
            options={
                'verbose_name': 'Logradouro',
                'verbose_name_plural': 'Logradouros',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('full_name', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('cpf_patient', models.CharField(max_length=11, unique=True, verbose_name='CPF')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('date_birth', models.DateField(verbose_name='Data de Nascimento')),
                ('local_birth', models.CharField(max_length=60, verbose_name='Local de Nascimento')),
                ('address_number', models.CharField(default='S/N', max_length=6, verbose_name='Número do Endereço')),
                ('address_cep', models.CharField(default='64600000', max_length=8, verbose_name='Cep do Endereço')),
                ('address_name', models.CharField(max_length=60, verbose_name='Endereço')),
                ('address_complement', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento do Endereço')),
                ('address_neighborhood', models.CharField(max_length=45, verbose_name='Bairro do Endereço')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='email')),
                ('phone_number_main', models.CharField(max_length=13, unique=True, verbose_name='Número de telefone (principal)')),
                ('phone_type_main', models.CharField(choices=[('CELL', 'CELL'), ('RESIDENCIAL', 'RESIDENCIAL'), ('COMERCIAL', 'COMERCIAL'), ('FAX', 'FAX')], default='CELL', max_length=11, verbose_name='Tipo de telefone')),
                ('phone_number_optional', models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='Número de telefone (opcional)')),
                ('phone_type_optional', models.CharField(blank=True, choices=[('CELL', 'CELL'), ('RESIDENCIAL', 'RESIDENCIAL'), ('COMERCIAL', 'COMERCIAL'), ('FAX', 'FAX')], max_length=11, null=True, verbose_name='Tipo de telefone')),
                ('image_patient', models.ImageField(blank=True, null=True, upload_to='patient/image', verbose_name='Imagem do Paciente')),
                ('City_codIBGE', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.City', verbose_name='Cidade')),
                ('Color_idColor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Color', verbose_name='Cor')),
                ('Marital_State_idMarital_State', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.MaritalState', verbose_name='Estado Conjugal')),
                ('Medical_Insurance_idMedical_insurance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.MedicalInsurance', verbose_name='Convênio')),
                ('Ocupation_idOcupation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Ocupation', verbose_name='Ocupação')),
                ('Type_Logradouro_idLogradouro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.TypeLogradouro', verbose_name='Logradouro')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='city',
            name='State_codIBGE_UF',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.State', verbose_name='Estado'),
        ),
    ]
