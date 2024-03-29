# Generated by Django 4.1.6 on 2023-05-03 07:17a

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0068_alter_superpower_last_checkout_marketsent'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketsent',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 3, 7, 17, 40, 939575, tzinfo=datetime.timezone.utc)),
        ),
    ]
