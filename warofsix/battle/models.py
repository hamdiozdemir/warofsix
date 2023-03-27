from django.db import models
from django.contrib.auth.models import User
from main.models import Troops, UserTroops, UserHeroes

# Create your models here.

class Battles(models.Model):
    attacker = models.ForeignKey(User, related_name="attacker", on_delete=models.SET_NULL, null=True)
    defender = models.ForeignKey(User, related_name="defender", on_delete=models.SET_NULL, null=True)
    auto = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attacker} TO {self.defender} at: {self.time}"
    
    @property
    def attacker_group(self):
        attacker = AttackerDeads.objects.filter(battle=self)
        return attacker
    
    @property
    def defender_group(self):
        defender = DefenderDeads.objects.filter(battle=self)
        return defender


class AttackerDeads(models.Model):
    battle = models.ForeignKey(Battles, on_delete=models.SET_NULL, null=True)
    user_troop = models.ForeignKey(UserTroops, on_delete=models.SET_NULL, null=True)
    troop_count = models.PositiveIntegerField(default=0)
    deads = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default="dead")
    user_hero = models.ForeignKey(UserHeroes, on_delete=models.CASCADE, blank=True, null=True)
    user_hero_troop = models.ForeignKey(Troops, on_delete=models.CASCADE, blank=True, null=True)
    user_hero_troop_count = models.PositiveIntegerField(default=0)
    user_hero_troop_dead = models.PositiveIntegerField(default=0)


    @property
    def troop_alive(self):
        return self.troop_count - self.deads
    
    @property
    def user_hero_troop_alive(self):
        return self.user_hero_troop_count - self.user_hero_troop_dead


class DefenderDeads(models.Model):
    battle = models.ForeignKey(Battles, on_delete=models.SET_NULL, null=True)
    user_troop = models.ForeignKey(UserTroops, on_delete=models.SET_NULL, null=True)
    troop_count = models.PositiveIntegerField(default=0)
    deads = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default="dead")
    user_hero = models.ForeignKey(UserHeroes, on_delete=models.CASCADE, blank=True, null=True)
    user_hero_troop = models.ForeignKey(Troops, on_delete=models.CASCADE, blank=True, null=True)
    user_hero_troop_count = models.PositiveIntegerField(default=0)
    user_hero_troop_dead = models.PositiveIntegerField(default=0)


    @property
    def troop_alive(self):
        return self.troop_count - self.deads
    
    @property
    def user_hero_troop_alive(self):
        return self.user_hero_troop_count - self.user_hero_troop_dead
