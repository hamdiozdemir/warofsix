# Generated by Django 4.1.6 on 2023-04-11 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_alter_resources_token'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alliances', '0005_alliancemembers_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllianceDepartingCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto', models.BooleanField(default=True)),
                ('time_left', models.PositiveIntegerField(default=0)),
                ('arriving_time', models.DateTimeField(auto_now_add=True)),
                ('campaign_type', models.CharField(default='', max_length=20)),
                ('is_completed', models.BooleanField(default=False)),
                ('creator_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('main_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departing_location', to='main.location')),
                ('target_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_location', to='main.location')),
            ],
        ),
        migrations.CreateModel(
            name='AllianceDepartingTroops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField(default=0)),
                ('campaign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='alliances.alliancedepartingcampaign')),
                ('user_troop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.usertroops')),
            ],
        ),
        migrations.CreateModel(
            name='AllianceDeoartingHeroes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alliances.alliancedepartingcampaign')),
                ('user_hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userheroes')),
            ],
        ),
    ]
