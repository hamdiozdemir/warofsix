# Generated by Django 4.1.6 on 2023-05-01 20:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_alter_messages_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 1, 20, 43, 40, 657587, tzinfo=datetime.timezone.utc)),
        ),
    ]