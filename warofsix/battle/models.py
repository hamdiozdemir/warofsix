from django.db import models
from django.contrib.auth.admin import User
from main.models import Troops, UserTroops

# Create your models here.

class Battles(models.Model):
    attacker = models.ForeignKey(User, related_name="attacker", on_delete=models.SET_NULL, null=True)
    defender = models.ForeignKey(User, related_name="defender", on_delete=models.SET_NULL, null=True)
    auto = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attacker} TO {self.defender} at: {self.time}"


class AttackerDeads(models.Model):
    battle = models.ForeignKey(Battles, on_delete=models.SET_NULL, null=True)
    troop = models.ForeignKey(UserTroops, on_delete=models.SET_NULL, null=True)
    current = models.PositiveIntegerField(default=0)
    deads = models.PositiveIntegerField(default=0)

    @property
    def alive(self):
        return self.current - self.deads


class DefenderDeads(models.Model):
    battle = models.ForeignKey(Battles, on_delete=models.SET_NULL, null=True)
    troop = models.ForeignKey(UserTroops, on_delete=models.SET_NULL, null=True)
    current = models.PositiveIntegerField(default=0)
    deads = models.PositiveIntegerField(default=0)

    @property
    def alive(self):
        return self.current - self.deads
