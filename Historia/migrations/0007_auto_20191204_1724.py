# Generated by Django 2.2.6 on 2019-12-04 17:24

import Historia.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historia', '0006_auto_20191204_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='pic',
            field=models.ImageField(upload_to=Historia.models.upload_location),
        ),
    ]
