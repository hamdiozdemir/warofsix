# Generated by Django 4.1.6 on 2023-04-19 08:42a

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_superpowerreports_revealed_attack_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 19, 8, 42, 44, 917509, tzinfo=datetime.timezone.utc)),
        ),
    ]
