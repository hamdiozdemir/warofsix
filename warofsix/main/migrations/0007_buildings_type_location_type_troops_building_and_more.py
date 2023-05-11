# Generated by Django 4.1.6 on 2023-02-17 10:54a

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_rename_rock_buildings_stone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildings',
            name='type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='type',
            field=models.CharField(default='wild', max_length=20),
        ),
        migrations.AddField(
            model_name='troops',
            name='building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.buildings'),
        ),
        migrations.AlterField(
            model_name='location',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
