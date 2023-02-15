from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserTroops, Race, Troops

@receiver(post_save, sender=Race)
def create_instances(sender, instance, created, **kwargs):
    if created:
        print("ÇALIŞTI-----------------")
        race = instance.name
        troops = Troops.objects.filter(race=race)
        user = instance.user
        for troop in troops:
            UserTroops.objects.create(user=user, troop = troop)
