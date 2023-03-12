from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone



# Create your models here.

class Race(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins"),
        ("Wild", "Wild"),
        ("Wild2", "Wild2")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=RACE_CHOICES)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Location(models.Model):
    TYPE_CHOICES = [
        ("settlement", "settlement"),
        ("wild", "wild"),
        ("nature", "nature")
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    locx = models.IntegerField()
    locy = models.IntegerField()
    location_name = models.CharField(max_length=30, default="Middle Earth")
    type = models.CharField(max_length=20, default="wild")


    def __str__(self):
        return f"User:{self.user} - X:{self.locx}, Y:{self.locy}; Type: {self.type}"
    

class Buildings(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins"),
        ("Wild", "Wild"),
        ("Wild2", "Wild2")
    ]
    race = models.CharField(max_length=80, choices=RACE_CHOICES)
    name = models.CharField(max_length=70)
    type = models.CharField(max_length=20, blank=True, null=True)
    health = models.IntegerField()
    wood = models.PositiveIntegerField()
    stone = models.PositiveIntegerField()
    iron = models.PositiveIntegerField()
    grain = models.PositiveIntegerField()
    update_time = models.PositiveIntegerField(default=0)
    sorting = models.PositiveIntegerField(default=0)    

    def __str__(self):
        return self.name


class Troops(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins"),
        ("Wild", "Wild"),
        ("Wild2", "Wild2"),
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
    crash_bonus = models.PositiveIntegerField(default=0)
    speed = models.FloatField()
    wood = models.PositiveIntegerField()
    stone = models.PositiveIntegerField()
    iron = models.PositiveIntegerField()
    grain = models.PositiveIntegerField()
    consuption = models.PositiveIntegerField()
    burden = models.PositiveIntegerField()
    building = models.ForeignKey(Buildings, on_delete=models.SET_NULL, blank=True, null=True)
    training_time = models.PositiveIntegerField(default=0)
    prerequisite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Heroes(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins"),
        ("Wild", "Wild"),
        ("Wild2", "Wild2"),
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
    name = models.CharField(max_length=70)
    race = models.CharField(max_length=80, choices=RACE_CHOICES)
    token = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=70, choices=TYPE_CHOICES)
    health = models.PositiveIntegerField()
    regenerate_time = models.PositiveIntegerField(default=43200)
    damage = models.FloatField()
    crash_bonus = models.PositiveIntegerField(default=0)
    speed = models.FloatField()
    infantry_attack_bonus = models.FloatField(default=1.00)
    infantry_defence_bonus = models.FloatField(default=1.00)
    pike_attack_bonus = models.FloatField(default=1.00)
    pike_defence_bonus = models.FloatField(default=1.00)
    archer_attack_bonus = models.FloatField(default=1.00)
    archer_defence_bonus = models.FloatField(default=1.00)
    cavalry_attack_bonus = models.FloatField(default=1.00)
    cavalry_defence_bonus = models.FloatField(default=1.00)
    monster_attack_bonus = models.FloatField(default=1.00)
    monster_defence_bonus = models.FloatField(default=1.00)
    summon_type = models.ForeignKey(Troops, on_delete=models.SET_NULL, null=True, blank=True)
    summon_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class UserHeroes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hero = models.ForeignKey(Heroes, on_delete=models.CASCADE)
    is_dead = models.BooleanField(default=False)
    current_health = models.PositiveIntegerField(blank=True)
    position = models.PositiveIntegerField(default=0)
    regenerate_time_left = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hero} ({self.user})"
    
    def save(self, *args, **kwargs):
        if not self.current_health:
            self.current_health = self.hero.health
        super(UserHeroes, self).save(*args, **kwargs)








class UserTroops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    troop = models.ForeignKey(Troops, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    defence_level = models.FloatField(default=1.00)
    attack_level = models.FloatField(default=1.00)
    training = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)
    time_passed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.troop.race} - {self.troop.name}"


class UserBuildings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    worker = models.PositiveIntegerField(default=0, blank=True, null=True)
    last_checkout = models.DateTimeField(auto_now_add=True)
    time_left = models.PositiveIntegerField(default=0)

    resource_worker = models.PositiveIntegerField(default=0)



    def __str__(self):
        return self.building.name
    

    @property
    def finish(self):
        fin = timezone.now() + timezone.timedelta(seconds=self.time_left)
        return fin

    @property
    def next_level(self):
        
        return self.level + 1
    
    @property
    def update_wood(self):
        return round((self.level +1) * 1.5 * self.building.wood)
    
    @property
    def update_stone(self):
        return round((self.level +1) * 1.5 * self.building.stone)
    
    @property
    def update_iron(self):
        return round((self.level +1) * 1.5 * self.building.iron)
    
    @property
    def update_grain(self):
        return round((self.level +1) * 1.5 * self.building.grain)
    

class UserTroopTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_building = models.ForeignKey(UserBuildings, on_delete=models.CASCADE)
    troop = models.ForeignKey(Troops, on_delete=models.CASCADE)

    training = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)
    time_passed = models.PositiveIntegerField(default=0)


class TroopUpgrades(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    banner_carrier = models.PositiveIntegerField(default=0)
    forge_blade = models.PositiveIntegerField(default=0)
    heavy_armor = models.PositiveIntegerField(default=0)
    arrow = models.PositiveIntegerField(default=0)

    upgrading_field = models.CharField(max_length=20, blank=True, null=True)
    time_left= models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)

    @property
    def bc_duration(self):
        return self.banner_carrier * 21 if self.banner_carrier != 0 else 21
    @property
    def fb_duration(self):
        return self.forge_blade * 21 if self.forge_blade != 0 else 21
    @property
    def ha_duration(self):
        return self.heavy_armor * 21 if self.heavy_armor != 0 else 21
    @property
    def fa_duration(self):
        return self.arrow * 21 if self.arrow != 0 else 21
    
    @property
    def bc_resource(self):
        return self.banner_carrier * 2000 if self.banner_carrier != 0 else 2000
    @property
    def fb_resource(self):
        return self.forge_blade * 2000 if self.forge_blade != 0 else 2000
    @property
    def ha_resource(self):
        return self.heavy_armor * 2000 if self.heavy_armor != 0 else 2000
    @property
    def fa_resource(self):
        return self.arrow  * 2000 if self.arrow != 0 else 2000
    

class Messages(models.Model):
    sender = models.ForeignKey(User, related_name='sender_user', on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='target_user', on_delete=models.CASCADE)
    header = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender} TO {self.target} - {self.header}"


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



class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    infantry_kill = models.PositiveIntegerField(default=0)
    pikeman_kill = models.PositiveIntegerField(default=0)
    archer_kill = models.PositiveIntegerField(default=0)
    cavalry_kill = models.PositiveIntegerField(default=0)
    siege_kill = models.PositiveIntegerField(default=0)
    infantry_dead = models.PositiveIntegerField(default=0)
    pikeman_dead = models.PositiveIntegerField(default=0)
    archer_dead = models.PositiveIntegerField(default=0)
    cavalry_dead = models.PositiveIntegerField(default=0)
    siege_dead = models.PositiveIntegerField(default=0)

    @property
    def total_kill(self):
        return sum((self.infantry_kill, self.pikeman_kill, self.archer_kill, self.cavalry_kill, self.siege_kill))
    
    @property
    def total_dead(self):
        return sum((self.infantry_dead, self.pikeman_dead, self.archer_dead, self.cavalry_dead, self.siege_dead))
    
    def __str__(self):
        return f"{self.user}'s Statistic"



class UserTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.PositiveIntegerField(default=0)



class Settlement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(UserBuildings, on_delete=models.SET_NULL, blank=True, null=True)
    settlement_id = models.IntegerField()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    description = models.CharField(max_length=280, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.race}"