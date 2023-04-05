from django.db import models
from django.contrib.auth.models import User
from main.models import UserTroops, Location
from django.db.models import Min
import math


# Create your models here.

class DepartingCampaigns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_location = models.ForeignKey(Location, related_name="departing_main_location", on_delete=models.CASCADE)
    target_location = models.ForeignKey(Location, related_name="departing_target_location", on_delete=models.CASCADE)
    auto = models.BooleanField(default=True)
    time_left = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)
    arriving_time = models.DateTimeField()
    campaign_type = models.CharField(max_length=20, default="")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} TO {self.target_location}"

    @property
    def distance(self):
        return round(((abs(self.main_location.locx - self.target_location.locx) ** 2) + (abs(self.main_location.locy - self.target_location.locy) ** 2)) ** 0.5, 2)
    
    @property
    def speed(self):
        troops = DepartingTroops.objects.filter(campaign=self).exclude(count=0)
        speeds = []
        for troop in troops:
            speeds.append(troop.user_troop.troop.speed)
        try:
            return min(speeds)
        except:
            return 10
    
    @property
    def group(self):
        group = DepartingTroops.objects.filter(campaign=self).order_by('position')
        return group
    

class DepartingTroops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    user_troop = models.ForeignKey(UserTroops, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    campaign = models.ForeignKey(DepartingCampaigns, on_delete=models.CASCADE, null=True)


class ArrivingCampaigns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_location = models.ForeignKey(Location, related_name="arriving_main_location", on_delete=models.CASCADE)
    target_location = models.ForeignKey(Location, related_name="arriving_target_location", on_delete=models.CASCADE)
    time_left = models.PositiveIntegerField(default=0)
    last_checkout = models.DateTimeField(auto_now_add=True)
    campaign_type = models.CharField(max_length=20, default="")
    arriving_wood = models.PositiveIntegerField(default=0)
    arriving_stone = models.PositiveIntegerField(default=0)
    arriving_iron = models.PositiveIntegerField(default=0)
    arriving_grain = models.PositiveIntegerField(default=0)
    arriving_time = models.DateTimeField(null=True, blank=True)

    @property
    def distance(self):
        return round(((abs(self.main_location.locx - self.target_location.locx) ** 2) + (abs(self.main_location.locy - self.target_location.locy) ** 2)) ** 0.5, 2)
    
    @property
    def speed(self):
        min_speed = ArrivingTroops.objects.exclude(user_troop__troop__speed=0).aggregate(Min('user_troop__troop__speed'))['user_troop__troop__speed__min']
        return min_speed
    
    @property
    def group(self):
        group = ArrivingTroops.objects.filter(campaign=self)
        return group


class ArrivingTroops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_troop = models.ForeignKey(UserTroops, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    campaign = models.ForeignKey(ArrivingCampaigns, on_delete=models.CASCADE, null=True)



class DefencePosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    user_troop = models.ForeignKey(UserTroops, on_delete=models.CASCADE)
    percent = models.PositiveIntegerField(default=0)


    @property
    def count(self):
        if self.user_troop.user == self.user:
            count = math.floor(self.user_troop.count * self.percent / 100)
        else:
            loc = Location.objects.get(user= self.user)
            troop = ReinforcementTroops.objects.get(location = loc, user_troop = self.user_troop)
            count = math.floor(troop.count * self.percent / 100)
        return count


class ReinforcementTroops(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user_troop = models.ForeignKey(UserTroops, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

