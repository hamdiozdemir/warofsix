from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class Race(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins")
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=RACE_CHOICES)


class Troops(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    type = models.CharField(max_length=70)
    health = models.IntegerField()
    damage = models.FloatField()
    speed = models.FloatField()
    wood = models.IntegerField()
    rock = models.IntegerField()
    iron = models.IntegerField()
    grain = models.IntegerField()


class Buildings(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    wood = models.IntegerField()
    rock = models.IntegerField()
    iron = models.IntegerField()
    grain = models.IntegerField()    


class UserTroops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    troop = models.ForeignKey(Troops, on_delete=models.CASCADE)
    count = models.IntegerField()
    level = models.FloatField(default=1.00)

class UserBuildings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)


class Mail(models.Model):
    sender = models.ManyToManyField(User, related_name='sender_user')
    target = models.ManyToManyField(User, related_name='targer_user')
    header = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    is_read = models.BooleanField(default=False)


class Resources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wood = models.IntegerField(default=800)
    rock = models.IntegerField(default=800)
    iron = models.IntegerField(default=800)
    grain = models.IntegerField(default=800)
    token = models.IntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)


class Market(models.Model):
    RESOURCE_CHOICES = [
        ("Wood", "Wood"),
        ("Rock", "Rock"),
        ("Iron", "Iron"),
        ("Grain", "Grain")
    ]
    offer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    offer_amount = models.IntegerField()
    target_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    target_amount = models.IntegerField()
    is_complete = models.BooleanField(default=False)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locx = models.IntegerField()
    locy = models.IntegerField()
    

class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    infantry_kill = models.IntegerField()
    pikeman_kill = models.IntegerField()
    archer_kill = models.IntegerField()
    cavalry_kill = models.IntegerField()
    siege_kill = models.IntegerField()
    infantry_dead = models.IntegerField()
    pikeman_dead = models.IntegerField()
    archer_dead = models.IntegerField()
    cavalry_dead = models.IntegerField()
    siege_dead = models.IntegerField()