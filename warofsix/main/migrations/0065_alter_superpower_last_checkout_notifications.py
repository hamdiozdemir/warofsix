# Generated by Django 4.1.6 on 2023-05-02 11:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0064_alter_superpower_last_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 11, 48, 31, 789174, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battle', models.BooleanField(default=False)),
                ('alliance', models.BooleanField(default=False)),
                ('report', models.BooleanField(default=False)),
                ('messages', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
