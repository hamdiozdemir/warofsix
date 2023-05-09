from django.db import models
from django.contrib.auth.models import User
from main.models import Race, UserTroops, Location, UserHeroes




# Create your models here.


class Alliances(models.Model):
    SIDES = [
        ('Good', 'Good'),
        ('Evil', 'Evil')
    ]
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, null=True, blank=True)
    founder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    side = models.CharField(max_length=4, choices=SIDES)
    banner = models.CharField(max_length=25, default="default.png")

    def __str__(self):
        return f"{self.name} - {self.side}"
    
    def save(self, *args, **kwargs):
        founder_race = Race.objects.get(user = self.founder).name
        if founder_race in ["Men", "Elves", "Dwarves"]:
            self.side = "Good"
        else:
            self.side = "Evil"
        super(Alliances, self).save(*args, **kwargs)
    
    @property
    def members(self):
        try:
            all_members = AllianceMembers.objects.filter(alliance = self)
        except:
            all_members = None
        return all_members
    
    @property
    def size(self):
        return len(self.members)


class AllianceMembers(models.Model):
    alliance = models.ForeignKey(Alliances, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='member')

    def __str__(self):
        return f"{self.member} from {self.alliance}"
    
    def race(self):
        return Race.objects.get(user = self.member).name


class AllianceJoinRequest(models.Model):
    alliance = models.ForeignKey(Alliances, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.requester} To {self.alliance}"



class AllianceChats(models.Model):
    alliance = models.ForeignKey(Alliances, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)



# CO-OP CAMPAIGN MODELS


class AllianceDepartingCampaign(models.Model):
    alliance = models.ForeignKey(Alliances, on_delete=models.CASCADE)
    creator_user = models.ForeignKey(AllianceMembers, on_delete=models.CASCADE)
    main_location = models.ForeignKey(Location, related_name="departing_location", on_delete=models.CASCADE)
    target_location = models.ForeignKey(Location, related_name="target_location", on_delete=models.CASCADE)
    auto = models.BooleanField(default=True)
    time_left = models.PositiveIntegerField(default=0)
    arriving_time = models.DateTimeField(auto_now_add=True)
    campaign_type = models.CharField(max_length=20, default="")
    is_completed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" ({self.id}) {self.creator_user.member} vs. {self.target_location.user}"

    @property
    def distance(self):
        return round(((abs(self.main_location.locx - self.target_location.locx) ** 2) + (abs(self.main_location.locy - self.target_location.locy) ** 2)) ** 0.5, 2)
    
    @property
    def speed(self):
        troops = AllianceDepartingTroops.objects.filter(campaign=self).exclude(count=0)
        speeds = []
        for troop in troops:
            speeds.append(troop.user_troop.troop.speed)
        try:
            return min(speeds)
        except:
            return 10

    @property
    def group(self):
        group = AllianceDepartingTroops.objects.filter(campaign=self).order_by('position')
        return group
    
    @property
    def heroes(self):
        departing_heroes = AllianceDepartingHeroes.objects.filter(campaign=self)
        return departing_heroes




class AllianceDepartingTroops(models.Model):
    position = models.PositiveIntegerField()
    user_troop = models.ForeignKey(UserTroops, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    campaign = models.ForeignKey(AllianceDepartingCampaign, on_delete=models.CASCADE, null=True)


class AllianceDepartingHeroes(models.Model):
    position = models.PositiveIntegerField()
    user_hero = models.ForeignKey(UserHeroes, on_delete=models.CASCADE)
    campaign = models.ForeignKey(AllianceDepartingCampaign, on_delete=models.CASCADE)
    
