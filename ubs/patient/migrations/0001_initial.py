# Generated by Django 2.2.6 on 2020-02-01 20:05

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('codIBGE7', models.IntegerField(verbose_name='Código IBGE7')),
                ('name_city', models.CharField(max_length=45, verbose_name='Nome da cidade')),
                ('port', models.CharField(max_length=20, verbose_name='Porta')),
                ('capital', models.CharField(max_length=12, verbose_name='Capital')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('name_color', models.CharField(max_length=45, verbose_name='Cor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaritalState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_marital_state', models.CharField(max_length=45, verbose_name='Estado Conjugal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicalInsurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_medical_insurance', models.CharField(max_length=13, verbose_name='Convênio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ocupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_ocupation', models.CharField(max_length=60, verbose_name='Ocupação')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('full_name', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('cpf_patient', models.CharField(max_length=100, verbose_name='cpf')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1, verbose_name='Sexo')),
                ('date_birth', models.DateField(verbose_name='Data de Nascimento')),
                ('local_birth', models.CharField(max_length=60, verbose_name='Local de Nascimento')),
                ('address_name', models.CharField(max_length=60, verbose_name='Nome do Endereço')),
                ('address_numero', models.CharField(max_length=6, verbose_name='Número do Endereço')),
                ('address_complement', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento do Endereço')),
                ('address_cep', models.CharField(max_length=8, verbose_name='cep do Endereço')),
                ('address_neighborhood', models.CharField(max_length=45, verbose_name='Vizinhança do Endereço')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='email')),
                ('city_cod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.City', verbose_name='Cidade')),
                ('color_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Color', verbose_name='Cor')),
                ('marital_state_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.MaritalState', verbose_name='Estado Conjugal')),
                ('medical_Insurance_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.MedicalInsurance', verbose_name='Convênio')),
                ('ocupation_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Ocupation', verbose_name='Ocupação')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('state', models.CharField(max_length=50, verbose_name='Estado')),
                ('UF', models.CharField(max_length=2, verbose_name='UF')),
                ('region', models.CharField(max_length=25, verbose_name='Região')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeLogradouro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_logradouro', models.CharField(max_length=45, verbose_name='Logradouro')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Autalizado em')),
                ('phone_number', models.CharField(max_length=13, verbose_name='Número de telefone')),
                ('phone_type', models.CharField(max_length=11, verbose_name='Tipo de telefone')),
                ('patient_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Patient', verbose_name='Telefone')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='type_Logradouro_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.TypeLogradouro', verbose_name='Logradouro'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.State', verbose_name='Estado'),
        ),
    ]
