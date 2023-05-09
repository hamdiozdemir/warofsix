from django.db import models
from django.contrib.auth.models import User
from main.models import Race, Location, Statistic, UserBuildings
from alliances.models import Alliances


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    alliance = models.ForeignKey(Alliances, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    description = models.CharField(max_length=280, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.race}"
    
    @property
    def side(self):
        race = self.race.name
        if race in ["Men", "Elves", "Dwarves"]:
            return "Good"
        else:
            return "Evil"
    
    @property
    def size_number(self):
        level_sum = sum([user_building.level for user_building in UserBuildings.objects.filter(user=self.user)])
        return level_sum

    
