# Generated by Django 2.2.6 on 2020-02-03 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_query', '0003_auto_20200203_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='phisicalexam',
            name='heigth',
            field=models.CharField(default=1, max_length=45, verbose_name='Altura(cm)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phisicalexam',
            name='weigth',
            field=models.CharField(default=1, max_length=45, verbose_name='Peso'),
            preserve_default=False,
        ),
    ]