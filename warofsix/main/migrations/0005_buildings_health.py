# Generated by Django 4.1.6 on 2023-02-15 13:48a

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userbuildings_worker_alter_troops_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildings',
            name='health',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
