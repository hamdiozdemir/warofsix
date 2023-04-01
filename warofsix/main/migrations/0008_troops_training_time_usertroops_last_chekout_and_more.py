# Generated by Django 4.1.6 on 2023-02-19 12:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_buildings_type_location_type_troops_building_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='troops',
            name='training_time',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usertroops',
            name='last_chekout',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertroops',
            name='training',
            field=models.PositiveIntegerField(default=0),
        ),
    ]