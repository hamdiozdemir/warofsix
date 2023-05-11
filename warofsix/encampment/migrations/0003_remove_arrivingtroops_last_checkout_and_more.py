# Generated by Django 4.1.6 on 2023-03-01 21:43a

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0031_alter_buildings_race_alter_troops_race'),
        ('encampment', '0002_arrivingtroops_target_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrivingtroops',
            name='last_checkout',
        ),
        migrations.RemoveField(
            model_name='arrivingtroops',
            name='target_location',
        ),
        migrations.RemoveField(
            model_name='arrivingtroops',
            name='time_left',
        ),
        migrations.RemoveField(
            model_name='departingtroops',
            name='last_checkout',
        ),
        migrations.RemoveField(
            model_name='departingtroops',
            name='target_location',
        ),
        migrations.RemoveField(
            model_name='departingtroops',
            name='time_left',
        ),
        migrations.CreateModel(
            name='DepartingCampaigns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_left', models.PositiveIntegerField(default=0)),
                ('last_checkout', models.DateTimeField(auto_now_add=True)),
                ('main_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departing_main_location', to='main.location')),
                ('target_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departing_target_location', to='main.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArrivingCampaigns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_left', models.PositiveIntegerField(default=0)),
                ('last_checkout', models.DateTimeField(auto_now_add=True)),
                ('main_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arriving_main_location', to='main.location')),
                ('target_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arriving_target_location', to='main.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='arrivingtroops',
            name='campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='encampment.arrivingcampaigns'),
        ),
        migrations.AddField(
            model_name='departingtroops',
            name='campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='encampment.departingcampaigns'),
        ),
    ]
