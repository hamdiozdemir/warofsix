# Generated by Django 4.1.6 on 2023-02-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_troopupgrades_last_checkout_troopupgrades_time_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='troopupgrades',
            name='upgrading_field',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]