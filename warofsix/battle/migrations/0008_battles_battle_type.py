# Generated by Django 4.1.6 on 2023-05-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0007_battlepillageresources'),
    ]

    operations = [
        migrations.AddField(
            model_name='battles',
            name='battle_type',
            field=models.CharField(default='', max_length=20),
        ),
    ]
