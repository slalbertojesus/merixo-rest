# Generated by Django 2.2.6 on 2019-11-19 19:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0002_auto_20191119_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='listaUsuarios',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, null=True, size=None),
        ),
    ]
