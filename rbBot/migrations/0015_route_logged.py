# Generated by Django 3.2 on 2021-07-02 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbBot', '0014_alter_route_destinations'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='logged',
            field=models.BooleanField(default=False),
        ),
    ]