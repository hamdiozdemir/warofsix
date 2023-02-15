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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=RACE_CHOICES)
    is_selected = models.BooleanField(default=False)


class Troops(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins")
    ]

    TYPE_CHOICES = [
        ("builder", "builder"),
        ("infantry", "infantry"),
        ("pike", "pike"),
        ("archer", "archer"),
        ("cavalry", "cavalry"),
        ("siege", "siege"),
        ("monster", "monster"),
    ]
    race = models.CharField(max_length=80, choices=RACE_CHOICES)
    name = models.CharField(max_length=70)
    type = models.CharField(max_length=70, choices=TYPE_CHOICES)
    health = models.PositiveIntegerField()
    damage = models.FloatField()
    speed = models.FloatField()
    wood = models.PositiveIntegerField()
    stone = models.PositiveIntegerField()
    iron = models.PositiveIntegerField()
    grain = models.PositiveIntegerField()
    consuption = models.PositiveIntegerField()
    burden = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Buildings(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins")
    ]
    race = models.CharField(max_length=80, choices=RACE_CHOICES)
    name = models.CharField(max_length=70)
    health = models.IntegerField()
    wood = models.PositiveIntegerField()
    stone = models.PositiveIntegerField()
    iron = models.PositiveIntegerField()
    grain = models.PositiveIntegerField()    


class UserTroops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    troop = models.ForeignKey(Troops, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    level = models.FloatField(default=1.00)

class UserBuildings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    worker = models.PositiveIntegerField(default=0, blank=True, null=True)


class Mail(models.Model):
    sender = models.ManyToManyField(User, related_name='sender_user')
    target = models.ManyToManyField(User, related_name='targer_user')
    header = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    is_read = models.BooleanField(default=False)


class Resources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wood = models.PositiveIntegerField(default=800)
    stone = models.PositiveIntegerField(default=800)
    iron = models.PositiveIntegerField(default=800)
    grain = models.PositiveIntegerField(default=800)
    token = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)


class Market(models.Model):
    RESOURCE_CHOICES = [
        ("Wood", "Wood"),
        ("Stone", "Stone"),
        ("Iron", "Iron"),
        ("Grain", "Grain")
    ]
    offer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    offer_amount = models.PositiveIntegerField()
    target_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    target_amount = models.PositiveIntegerField()
    is_complete = models.BooleanField(default=False)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locx = models.IntegerField()
    locy = models.IntegerField()
    

class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    infantry_kill = models.PositiveIntegerField()
    pikeman_kill = models.PositiveIntegerField()
    archer_kill = models.PositiveIntegerField()
    cavalry_kill = models.PositiveIntegerField()
    siege_kill = models.PositiveIntegerField()
    infantry_dead = models.PositiveIntegerField()
    pikeman_dead = models.PositiveIntegerField()
    archer_dead = models.PositiveIntegerField()
    cavalry_dead = models.PositiveIntegerField()
    siege_dead = models.PositiveIntegerField()


