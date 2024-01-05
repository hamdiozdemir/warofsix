from .models import Resources, UserTroops, WildData
from django.utils import timezone
from datetime import timedelta


class WildUpdates():

    def __init__(self, wild_user):
        self.wild_user = wild_user
        self.wild_data_object = WildData.objects.get(user = self.wild_user)

    
    def resource_update(self):
        # convert to hour bcoz troop production number is per hour on DB
        time_passed = (timezone.now() - self.wild_data_object.resource_last_checkout).total_seconds() / 3600
        production = round(time_passed * self.wild_data_object.resource_production_number)

        if production == 0:
            pass
        else:
            wild_resources = Resources.objects.get(user=self.wild_user)
            wild_resources.wood += production
            wild_resources.stone += production
            wild_resources.iron += production
            wild_resources.grain += production
            wild_resources.save()
            self.wild_data_object.resource_last_checkout = timezone.now()
            self.wild_data_object.save()

    def troop_update(self):
        # convert to hour bcoz troop production number is per hour on DB
        time_passed = (timezone.now() - self.wild_data_object.troop_last_checkout).total_seconds() / 3600
        production = round(time_passed * self.wild_data_object.troop_production_number / 3)
        if production == 0:
            pass
        else:
            wild_troops = UserTroops.objects.filter(user=self.wild_user)
            for troop in wild_troops:
                troop.count += production
                troop.save()
            self.wild_data_object.troop_last_checkout = self.wild_data_object.troop_last_checkout + timedelta(hours= production * self.wild_data_object.troop_production_number)
            self.wild_data_object.save()
        
    
    def combine_resource_troop_update(self):
        # convert to hour bcoz troop production number is per hour on DB
        resource_time_passed = (timezone.now() - self.wild_data_object.resource_last_checkout).total_seconds() / 3600
        resource_time_passed = resource_time_passed 
        resource_production = round(resource_time_passed * self.wild_data_object.resource_production_number)

        troop_time_passed = (timezone.now() - self.wild_data_object.troop_last_checkout).total_seconds() / 3600
        troop_production = round(troop_time_passed * self.wild_data_object.troop_production_number / 3)
        if resource_production == 0:
            pass
        else:
            wild_resources = Resources.objects.get(user=self.wild_user)
            wild_resources.wood += resource_production
            wild_resources.stone += resource_production
            wild_resources.iron += resource_production
            wild_resources.grain += resource_production
            wild_resources.save()
        if troop_production == 0:
            pass
        else:
            wild_troops = UserTroops.objects.filter(user=self.wild_user)
            for troop in wild_troops:
                troop.count += troop_production
                troop.save()
            
        self.wild_data_object.resource_last_checkout = timezone.now()
        self.wild_data_object.troop_last_checkout = self.wild_data_object.troop_last_checkout + timedelta(hours= troop_production * self.wild_data_object.troop_production_number)
        self.wild_data_object.save()


