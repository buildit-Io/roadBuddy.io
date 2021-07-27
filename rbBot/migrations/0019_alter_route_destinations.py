# Generated by Django 3.2 on 2021-07-23 18:28

from django.db import migrations, models
import rbBot.models


class Migration(migrations.Migration):

    dependencies = [
        ('rbBot', '0018_alter_route_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='destinations',
            field=models.JSONField(default=rbBot.models.destinations_default_value),
        ),
    ]