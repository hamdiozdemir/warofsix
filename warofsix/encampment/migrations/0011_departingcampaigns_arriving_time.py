# Generated by Django 4.1.6 on 2023-03-31 17:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encampment', '0010_alter_arrivingtroops_user_troop'),
    ]

    operations = [
        migrations.AddField(
            model_name='departingcampaigns',
            name='arriving_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 31, 17, 33, 26, 836375, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
