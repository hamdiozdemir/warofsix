# Generated by Django 4.1.6 on 2023-04-11 08:37a

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alliances', '0004_alliancechats'),
    ]

    operations = [
        migrations.AddField(
            model_name='alliancemembers',
            name='role',
            field=models.CharField(default='member', max_length=10),
        ),
    ]
