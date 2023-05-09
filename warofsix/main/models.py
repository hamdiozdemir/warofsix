from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta




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
        ("Evil", "Evil")
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
    has_ring = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} {self.locx}|{self.locy}"
    
    @property
    def race(self):
        if self.user:
            race = Race.objects.get(user=self.user)
            return race.name
        else:
            None
    

class Buildings(models.Model):
    RACE_CHOICES = [
        ("Men", "Men"),
        ("Elves", "Elves"),
        ("Dwarves", "Dwarves"),
        ("Isengard", "Isengard"),
        ("Mordor", "Mordor"),
        ("Goblins", "Goblins"),
        ("Wild", "Wild"),
        ("Dark", "Dark")
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
    description = models.CharField(max_length=140, default=" ")    

    def __str__(self):
        return self.name
    
    @property
    def damage(self):
        if self.type == "defence" and self.name != "Warg Sentry":
            if self.race == "Elves":
                return 300
            elif self.race == "Dwarves":
                return 230
            elif self.race == "Isengard" or self.race == "Mordor":
                return 220
            else:
                return 200
        elif self.type == "defence" and self.name == "Warg Sentry":
            return 400
        else:
            return 0
    


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
        ("Good", "Good"),
        ("Evil", "Evil")
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
    rings = models.PositiveIntegerField(default=0)
    the_one_ring = models.BooleanField(default=False)
    type = models.CharField(max_length=70, choices=TYPE_CHOICES)
    health = models.PositiveIntegerField()
    regenerate_time = models.PositiveIntegerField(default=43200)
    damage = models.PositiveIntegerField()
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
    
    def attack_bonus_types(self):
        fields = []
        if self.infantry_attack_bonus > 1:
            fields.append("Infantry")
        if self.pike_attack_bonus > 1:
            fields.append("Pike")
        if self.archer_attack_bonus > 1:
            fields.append("Archer")
        if self.cavalry_attack_bonus > 1:
            fields.append("Cavalary")
        if self.monster_attack_bonus > 1:
            fields.append("Monster")
        return ", ".join(fields)
    
    def defence_bonus_types(self):
        fields = []
        if self.infantry_defence_bonus > 1:
            fields.append("Infantry")
        if self.pike_defence_bonus > 1:
            fields.append("Pike")
        if self.archer_defence_bonus > 1:
            fields.append("Archer")
        if self.cavalry_defence_bonus > 1:
            fields.append("Cavalary")
        if self.monster_defence_bonus > 1:
            fields.append("Monster")
        return ", ".join(fields)

class UserHeroes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hero = models.ForeignKey(Heroes, on_delete=models.CASCADE)
    is_dead = models.BooleanField(default=False)
    is_home = models.BooleanField(default=True)
    current_health = models.PositiveIntegerField(blank=True)
    position = models.PositiveIntegerField(default=0)
    regenerate_time_left = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)

    @property
    def is_available(self):
        if not self.is_dead and self.is_home:
            return True
        else:
            return False
    
    @property
    def status(self):
        if self.is_dead:
            return "Dead"
        if not self.is_home:
            return "On A Journey"
        else:
            return "Available"

    def __str__(self):
        return f"{self.hero} ({self.user})"
    
    def save(self, *args, **kwargs):
        self.last_checkout = timezone.now()
        if not self.current_health and self.is_dead == False:
            self.current_health = self.hero.health
        if self.is_dead:
            self.is_home = True
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
        return f"{self.id}: {self.troop.race} - {self.troop.name}"


class UserBuildings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    worker = models.PositiveIntegerField(default=0, blank=True, null=True)
    last_checkout = models.DateTimeField(auto_now_add=True)
    time_left = models.PositiveIntegerField(default=0)

    resource_worker = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"({self.id}) {self.building.name}"
    

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
    
    @property
    def current_health(self):
        return self.building.health + 1500
    
    @property
    def user_building_damage(self):
        return self.building.damage * self.level * 0.75
    
        

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
    content = models.TextField(max_length=500)
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
    token = models.PositiveIntegerField(default=300)
    rings = models.PositiveIntegerField(default=0)
    the_one_ring = models.BooleanField(default=False)
    last_checkout = models.DateTimeField(auto_now_add=True)


class UserMarkets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_capacity = models.PositiveIntegerField(default=0)

    @property
    def offer_capacity(self):
        user_markets = UserBuildings.objects.filter(user=self.user, building__type = "market")
        if user_markets.exists():
            market_level = 0
            for market in user_markets:
                market_level += market.level
            return market_level * 50000
        else:
            return 0
    
    @property
    def current(self):
        total_offer_amount = Exchanges.objects.filter(offer_user=self.user, is_complete = False).aggregate(models.Sum('offer_amount'))['offer_amount__sum'] or 0
        total_on_way = MarketSent.objects.filter(sender=self.user, is_complete = False)
        total_on_way_burden = 0 if not total_on_way.exists() else sum([obj.total_burden for obj in total_on_way])

        return self.offer_capacity - total_offer_amount - total_on_way_burden




class Exchanges(models.Model):
    RESOURCE_CHOICES = [
        ("wood", "Wood"),
        ("stone", "Stone"),
        ("iron", "Iron"),
        ("grain", "Grain")
    ]
    offer_user = models.ForeignKey(User, related_name="offer_user", on_delete=models.CASCADE)
    offer_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    offer_amount = models.PositiveIntegerField()
    client_user = models.ForeignKey(User, related_name="client_user", on_delete=models.CASCADE, null=True, blank=True)
    target_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    target_amount = models.PositiveIntegerField()
    is_complete = models.BooleanField(default=False)
    added_time = models.DateTimeField(auto_now_add=True)
    

class MarketSent(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    target_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    wood = models.PositiveIntegerField(default=0)
    stone = models.PositiveIntegerField(default=0)
    iron = models.PositiveIntegerField(default=0)
    grain = models.PositiveIntegerField(default=0)
    time_left = models.PositiveIntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total_burden(self):
        return self.wood + self.stone + self.iron + self.grain

    @property
    def arriving_time(self):
        return self.timestamp + timedelta(seconds=self.time_left)


class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kill = models.PositiveIntegerField(default=0)
    dead = models.PositiveIntegerField(default=0)
    hero_kill = models.PositiveIntegerField(default=0)
    hero_dead = models.PositiveIntegerField(default=0)


    @property
    def total_kill(self):
        return self.kill
    
    @property
    def total_dead(self):
        return self.dead
    
    def __str__(self):
        return f"{self.user}'s Statistic"



class UserTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.PositiveIntegerField(default=0)



class Settlement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(UserBuildings, on_delete=models.SET_NULL, blank=True, null=True)
    settlement_id = models.IntegerField()


class WildData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_production_number = models.PositiveIntegerField(default=1)
    troop_production_number = models.PositiveIntegerField(default=1)
    resource_last_checkout = models.DateTimeField(auto_now_add=True)
    troop_last_checkout = models.DateTimeField(auto_now_add=True)


class SuperPower(models.Model):
    user_building = models.ForeignKey(UserBuildings, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    power_damage = models.PositiveIntegerField(default=20000)
    is_active = models.BooleanField(default=False)
    last_checkout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def next_round(self):
        if not self.is_active:
            return 86400
        else:
            time_left = round(((self.last_checkout + timedelta(days=1)) - timezone.now()).total_seconds())
            time_left = time_left if time_left > 0 else 0
            return time_left
    
    @property
    def power_reports(self):
        reports = SuperPowerReports.objects.filter(super_power = self)
        if reports.exists():
            return reports
        else:
            None



class SuperPowerReports(models.Model):
    super_power = models.ForeignKey(SuperPower, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    building = models.ForeignKey(Buildings, on_delete=models.SET_NULL, null=True, blank=True)
    pre_level = models.PositiveIntegerField(default=0)
    post_level = models.PositiveIntegerField(default=0)
    troop = models.ForeignKey(Troops, related_name="troop_to_death", on_delete=models.SET_NULL, null=True, blank=True)
    deads = models.PositiveIntegerField(default=0)
    revealed_troop = models.ForeignKey(Troops, related_name="troop_to_reveal", on_delete=models.SET_NULL, null=True, blank=True)
    revealed_count = models.PositiveIntegerField(default=0)
    revealed_attack_level = models.FloatField(default=1.0)
    revealed_defence_level = models.FloatField(default=1.0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"vs. {self.location.user} ({self.location.location_name})"
    
    def attacker_race(self):
        return self.super_power.user_building.building.race



class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alliance = models.BooleanField(default=False)
    report = models.BooleanField(default=False)
    messages = models.BooleanField(default=False)