# Generated by Django 4.1.6 on 2023-05-02 22:48a

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0067_remove_notifications_battle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 22, 48, 37, 161652, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='MarketSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wood', models.PositiveIntegerField(default=0)),
                ('stone', models.PositiveIntegerField(default=0)),
                ('iron', models.PositiveIntegerField(default=0)),
                ('grain', models.PositiveIntegerField(default=0)),
                ('time_left', models.PositiveIntegerField(default=0)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('target_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.location')),
            ],
        ),
    ]
