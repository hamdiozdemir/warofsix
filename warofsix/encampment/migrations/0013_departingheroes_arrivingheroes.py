# Generated by Django 4.1.6 on 2023-04-06 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_userheroes_is_home'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('encampment', '0012_remove_arrivingcampaigns_is_completed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartingHeroes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encampment.departingcampaigns')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userheroes')),
            ],
        ),
        migrations.CreateModel(
            name='ArrivingHeroes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encampment.arrivingcampaigns')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userheroes')),
            ],
        ),
    ]