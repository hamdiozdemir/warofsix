# Generated by Django 4.1.6 on 2023-04-07 23:06a

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_userheroes_is_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroes',
            name='damage',
            field=models.PositiveIntegerField(),
        ),
    ]
