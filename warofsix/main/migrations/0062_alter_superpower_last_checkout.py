# Generated by Django 4.1.6 on 2023-05-01 21:11a

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_alter_superpower_last_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 1, 21, 11, 8, 952116, tzinfo=datetime.timezone.utc)),
        ),
    ]
