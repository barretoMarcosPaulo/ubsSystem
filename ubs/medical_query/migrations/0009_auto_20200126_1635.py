# Generated by Django 2.2.6 on 2020-01-26 19:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medical_query', '0008_auto_20200126_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalquery',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 1, 26, 19, 35, 32, 352603, tzinfo=utc), verbose_name='Data'),
        ),
    ]
