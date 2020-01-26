# Generated by Django 2.2.6 on 2020-01-26 15:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medical_query', '0002_auto_20200125_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalquery',
            name='fc',
            field=models.CharField(default=1, max_length=50, verbose_name='FC(bpm)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicalquery',
            name='p',
            field=models.CharField(default=1, max_length=50, verbose_name='P(bpm)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicalquery',
            name='pa',
            field=models.CharField(default=1, max_length=50, verbose_name='PA(mmHg)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicalquery',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 1, 26, 15, 29, 16, 339613, tzinfo=utc), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='medicalquery',
            name='epidemiological_history',
            field=models.CharField(max_length=50, verbose_name='FR(irpm)'),
        ),
        migrations.AlterField(
            model_name='medicalquery',
            name='family_history',
            field=models.CharField(max_length=50, verbose_name='Peso(g)'),
        ),
        migrations.AlterField(
            model_name='medicalquery',
            name='physiological_personal_antecedents',
            field=models.CharField(max_length=50, verbose_name='Altura(cm)'),
        ),
        migrations.AlterField(
            model_name='medicalquery',
            name='previous_pathological_history',
            field=models.CharField(max_length=50, verbose_name='TAX(ºC)'),
        ),
        migrations.DeleteModel(
            name='PhysicalExam',
        ),
    ]