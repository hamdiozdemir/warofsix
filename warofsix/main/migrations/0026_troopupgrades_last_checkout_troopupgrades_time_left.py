# Generated by Django 4.1.6 on 2023-02-26 22:12a

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_userbuildings_training_checkout_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='troopupgrades',
            name='last_checkout',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='troopupgrades',
            name='time_left',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
