# Generated by Django 2.2.6 on 2019-12-04 17:34

import Usuario.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0005_auto_20191204_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pic',
            field=models.ImageField(default='/media/user.png', upload_to=Usuario.models.upload_location),
        ),
    ]