# Generated by Django 4.1.6 on 2023-05-06 15:23a

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_buildings_description_alter_superpower_last_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='has_ring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 6, 15, 23, 51, 113435, tzinfo=datetime.timezone.utc)),
        ),
    ]
