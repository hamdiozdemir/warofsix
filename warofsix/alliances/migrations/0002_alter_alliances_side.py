# Generated by Django 4.1.6 on 2023-04-08 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alliances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alliances',
            name='side',
            field=models.CharField(choices=[('Good', 'Good'), ('Evil', 'Evil')], max_length=4),
        ),
    ]
