# Generated by Django 4.1.6 on 2023-03-12 01:05a

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_alter_heroes_archer_attack_bonus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userheroes',
            name='current_health',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
