# Generated by Django 2.2.6 on 2019-12-03 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historia', '0004_like_already_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='already_liked',
            field=models.BooleanField(default=True),
        ),
    ]