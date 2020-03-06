# Generated by Django 2.2.6 on 2020-03-06 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CID10',
            fields=[
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('idCID10', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('desc_CID10', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExamRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_exam', models.CharField(max_length=255, verbose_name='Descrição do exame')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('full_name', models.CharField(max_length=100, verbose_name='Nome do remedio')),
                ('generic_name', models.CharField(max_length=100, verbose_name='Nome generico')),
                ('dosage', models.CharField(max_length=255, verbose_name='Dosagem')),
                ('unity', models.CharField(choices=[('CX', 'Caixa'), ('VD', 'Vidro'), ('FR', 'Frasco'), ('AM', 'Ampola'), ('CO', 'Comprimido')], max_length=3, verbose_name='Unidade')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhisicalExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('pa', models.CharField(blank=True, max_length=45, null=True, verbose_name='PA(mmHg)')),
                ('p', models.CharField(blank=True, max_length=45, null=True, verbose_name='P(bpm)')),
                ('fc', models.CharField(blank=True, max_length=50, null=True, verbose_name='FC(bpm)')),
                ('fr', models.CharField(blank=True, max_length=45, null=True, verbose_name='FR(irpm)')),
                ('tax', models.CharField(blank=True, max_length=50, null=True, verbose_name='TAX(ºC)')),
                ('weigth', models.CharField(blank=True, max_length=45, null=True, verbose_name='Peso')),
                ('heigth', models.CharField(blank=True, max_length=45, null=True, verbose_name='Altura(cm)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('type_query', models.IntegerField(choices=[(1, 'Consulta'), (2, 'Retorno')], verbose_name='Tipo de Consulta')),
                ('main_complaint', models.TextField(max_length=400, verbose_name='Queixa Principal')),
                ('current_health_history', models.TextField(max_length=400, verbose_name='História da Doença Atual')),
                ('review_of_systems', models.TextField(max_length=400, verbose_name='Revisão de Sistemas')),
                ('epidemiological_history', models.TextField(max_length=400, verbose_name='História Epidemiológica')),
                ('previous_pathological_history', models.TextField(max_length=400, verbose_name='História Patológica Regressa')),
                ('family_history', models.TextField(max_length=400, verbose_name='História Familiar')),
                ('physiological_personal_antecedents', models.TextField(max_length=400, verbose_name='Antecedentes Pessoais Fisiológicas')),
                ('summary', models.TextField(max_length=400, verbose_name='Sumário dos Postos Principais da História e Exame Físico')),
                ('diagnostic_hypotheses', models.TextField(max_length=400, verbose_name='Hipótese(s) Diagnósticada(s)')),
                ('take_duct', models.TextField(max_length=400, verbose_name='Conduta Tomada')),
                ('gestational_history', models.TextField(blank=True, max_length=400, null=True, verbose_name='História Gestacional')),
                ('repoductive_health', models.TextField(blank=True, max_length=400, null=True, verbose_name='Saúde Reprodutiva')),
                ('Patient_idPatient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Patient', verbose_name='Paciente')),
                ('PhisicalExam_idPhisicalExam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medical_query.PhisicalExam', verbose_name='Exame Físico')),
                ('User_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Doctor', verbose_name='Profissional')),
                ('cid10', models.ManyToManyField(related_name='cid10', to='medical_query.CID10', verbose_name='CID10')),
                ('examRequest', models.ManyToManyField(related_name='examRequest', to='medical_query.ExamRequest', verbose_name='Exame(s)')),
                ('medicine', models.ManyToManyField(related_name='medicine', to='medical_query.Medicine', verbose_name='Medicamento(s)')),
            ],
            options={
                'verbose_name': 'Consulta Medica',
                'verbose_name_plural': 'Consultas Medicas',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='QueryHasMedicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('amount', models.CharField(max_length=400, null=True, verbose_name='Pescrição')),
                ('Query_idQuery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medical_query.Query', verbose_name='Consulta')),
                ('medicine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medical_query.Medicine', verbose_name=' Medicamento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Forwarding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('in_attendance', models.BooleanField(default=False, verbose_name='Paciente em atendimento')),
                ('finalized', models.BooleanField(default=False, verbose_name='Finalizado')),
                ('priority', models.BooleanField(default=False, verbose_name='Paciente Prioritário')),
                ('medical', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Doctor', verbose_name='Profissional')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Patient', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Encaminhamento',
                'verbose_name_plural': 'Encaminhamentos',
                'ordering': ['created_on'],
            },
        ),
    ]
