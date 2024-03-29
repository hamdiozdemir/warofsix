# Generated by Django 4.1.6 on 2023-04-18 17:09a

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_resources_the_one_ring'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperPower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('last_checkout', models.DateTimeField(auto_now_add=True)),
                ('user_building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userbuildings')),
            ],
        ),
        migrations.CreateModel(
            name='SuperPowerReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_level', models.PositiveIntegerField(default=0)),
                ('post_level', models.PositiveIntegerField(default=0)),
                ('deads', models.PositiveIntegerField(default=0)),
                ('revealed_count', models.PositiveIntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.buildings')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.location')),
                ('revealed_troop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='troop_to_reveal', to='main.troops')),
                ('super_power', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.superpower')),
                ('troop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='troop_to_death', to='main.troops')),
            ],
        ),
    ]
