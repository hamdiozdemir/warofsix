# Generated by Django 4.1.6 on 2023-04-16 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_rename_last_checkout_wilddata_resource_last_checkout_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wilddata',
            name='troop_last_checkout',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
