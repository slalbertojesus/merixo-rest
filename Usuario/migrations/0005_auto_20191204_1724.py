# Generated by Django 2.2.6 on 2019-12-04 17:24

import Usuario.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0004_auto_20191202_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pic',
            field=models.ImageField(default='http://merixo.tk/media/user.png', upload_to=Usuario.models.upload_location),
        ),
    ]
