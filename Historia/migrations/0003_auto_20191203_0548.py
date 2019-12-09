# Generated by Django 2.2.6 on 2019-12-03 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Historia', '0002_story_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='story',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Historia.Story')),
            ],
        ),
    ]