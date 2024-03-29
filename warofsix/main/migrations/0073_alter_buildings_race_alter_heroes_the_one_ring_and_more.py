# Generated by Django 4.1.6 on 2023-05-07 17:02a

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0072_location_has_ring_alter_superpower_last_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildings',
            name='race',
            field=models.CharField(choices=[('Men', 'Men'), ('Elves', 'Elves'), ('Dwarves', 'Dwarves'), ('Isengard', 'Isengard'), ('Mordor', 'Mordor'), ('Goblins', 'Goblins'), ('Wild', 'Wild'), ('Dark', 'Dark')], max_length=80),
        ),
        migrations.AlterField(
            model_name='heroes',
            name='the_one_ring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='race',
            name='name',
            field=models.CharField(choices=[('Men', 'Men'), ('Elves', 'Elves'), ('Dwarves', 'Dwarves'), ('Isengard', 'Isengard'), ('Mordor', 'Mordor'), ('Goblins', 'Goblins'), ('Wild', 'Wild'), ('Dark', 'Dark')], max_length=100),
        ),
        migrations.AlterField(
            model_name='superpower',
            name='last_checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 7, 17, 2, 39, 4231, tzinfo=datetime.timezone.utc)),
        ),
    ]
