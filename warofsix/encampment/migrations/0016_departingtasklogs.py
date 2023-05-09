# Generated by Django 4.1.6 on 2023-05-01 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encampment', '0015_arrivingcampaigns_arriving_rings'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartingTaskLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=100)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_call_time', models.DateTimeField(auto_now_add=True)),
                ('departing_campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='encampment.departingcampaigns')),
            ],
        ),
    ]
