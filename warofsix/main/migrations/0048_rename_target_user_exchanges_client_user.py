# Generated by Django 4.1.6 on 2023-04-15 16:16a

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_exchanges_usermarkets_delete_market'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchanges',
            old_name='target_user',
            new_name='client_user',
        ),
    ]
