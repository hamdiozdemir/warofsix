# Generated by Django 4.1.6 on 2023-02-15 13:45a

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_troops_burden'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbuildings',
            name='worker',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='troops',
            name='type',
            field=models.CharField(choices=[('builder', 'builder'), ('infantry', 'infantry'), ('pike', 'pike'), ('archer', 'archer'), ('cavalry', 'cavalry'), ('siege', 'siege'), ('monster', 'monster')], max_length=70),
        ),
    ]
