# Generated by Django 4.1.6 on 2023-05-02 18:47aa

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0066_alter_superpower_last_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='battle',
        ),
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 18, 47, 6, 702526, tzinfo=datetime.timezone.utc)),
        ),
    ]
