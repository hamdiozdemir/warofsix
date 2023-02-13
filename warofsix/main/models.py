from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class Resource(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    last_generated_at = models.DateTimeField(auto_now_add=True)


class Race(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


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


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    is_read = models.BooleanField(default=False)


class Resources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wood = models.IntegerField(default=800)
    rock = models.IntegerField(default=800)
    iron = models.IntegerField(default=800)
    grain = models.IntegerField(default=800)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locx = models.IntegerField()
    locy = models.IntegerField()
    
