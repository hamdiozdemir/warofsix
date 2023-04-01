# Generated by Django 4.1.6 on 2023-03-02 12:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_alter_buildings_race_alter_troops_race'),
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='battles',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attackerdeads',
            name='troop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.usertroops'),
        ),
        migrations.AlterField(
            model_name='defenderdeads',
            name='troop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.usertroops'),
        ),
    ]