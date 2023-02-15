# Generated by Django 4.1.6 on 2023-02-14 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race', models.CharField(choices=[('Men', 'Men'), ('Elves', 'Elves'), ('Dwarves', 'Dwarves'), ('Isengard', 'Isengard'), ('Mordor', 'Mordor'), ('Goblins', 'Goblins')], max_length=80)),
                ('name', models.CharField(max_length=70)),
                ('wood', models.PositiveIntegerField()),
                ('rock', models.PositiveIntegerField()),
                ('iron', models.PositiveIntegerField()),
                ('grain', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Troops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race', models.CharField(choices=[('Men', 'Men'), ('Elves', 'Elves'), ('Dwarves', 'Dwarves'), ('Isengard', 'Isengard'), ('Mordor', 'Mordor'), ('Goblins', 'Goblins')], max_length=80)),
                ('name', models.CharField(max_length=70)),
                ('type', models.CharField(max_length=70)),
                ('health', models.PositiveIntegerField()),
                ('damage', models.FloatField()),
                ('speed', models.FloatField()),
                ('wood', models.PositiveIntegerField()),
                ('rock', models.PositiveIntegerField()),
                ('iron', models.PositiveIntegerField()),
                ('grain', models.PositiveIntegerField()),
                ('consuption', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserTroops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('level', models.FloatField(default=1.0)),
                ('troop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.troops')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBuildings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField(default=0)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.buildings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infantry_kill', models.PositiveIntegerField()),
                ('pikeman_kill', models.PositiveIntegerField()),
                ('archer_kill', models.PositiveIntegerField()),
                ('cavalry_kill', models.PositiveIntegerField()),
                ('siege_kill', models.PositiveIntegerField()),
                ('infantry_dead', models.PositiveIntegerField()),
                ('pikeman_dead', models.PositiveIntegerField()),
                ('archer_dead', models.PositiveIntegerField()),
                ('cavalry_dead', models.PositiveIntegerField()),
                ('siege_dead', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wood', models.PositiveIntegerField(default=800)),
                ('rock', models.PositiveIntegerField(default=800)),
                ('iron', models.PositiveIntegerField(default=800)),
                ('grain', models.PositiveIntegerField(default=800)),
                ('token', models.PositiveIntegerField(default=0)),
                ('last_checkout', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Men', 'Men'), ('Elves', 'Elves'), ('Dwarves', 'Dwarves'), ('Isengard', 'Isengard'), ('Mordor', 'Mordor'), ('Goblins', 'Goblins')], max_length=100)),
                ('is_selected', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_type', models.CharField(choices=[('Wood', 'Wood'), ('Rock', 'Rock'), ('Iron', 'Iron'), ('Grain', 'Grain')], max_length=50)),
                ('offer_amount', models.PositiveIntegerField()),
                ('target_type', models.CharField(choices=[('Wood', 'Wood'), ('Rock', 'Rock'), ('Iron', 'Iron'), ('Grain', 'Grain')], max_length=50)),
                ('target_amount', models.PositiveIntegerField()),
                ('is_complete', models.BooleanField(default=False)),
                ('offer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=400)),
                ('is_read', models.BooleanField(default=False)),
                ('sender', models.ManyToManyField(related_name='sender_user', to=settings.AUTH_USER_MODEL)),
                ('target', models.ManyToManyField(related_name='targer_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locx', models.IntegerField()),
                ('locy', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
