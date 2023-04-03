from main.models import UserTroops, Location
from .models import DefencePosition, DepartingCampaigns, DepartingTroops, ArrivingCampaigns, ArrivingTroops, ReinforcementTroops
from django.utils import timezone
from datetime import timedelta
from main.signals import campaign_created_signal

class TroopManagements():

    def __init__(self, data, user):
        self.data = data
        self.user = user
        self.user_troop_query = UserTroops.objects.filter(user=self.user)
        self.positions = [11,12,13,14,21,22,23,24,31,32,33,34]
    

    def defence_formation_percent_check(self):
        # filter the data with only troops
        filtered_data = {k:v for k,v in self.data.items() if k.startswith('troop')}
        # create a dict from unique troop id, value is 0 as the number
        new_data = dict.fromkeys(set(filtered_data.values()), 0)

        for k,v in filtered_data.items():
            if v in new_data.keys():
                new_data[v] += int(self.data["numd"+k[-2:]])
        if all(number <= 100 for number in new_data.values()):
            return True
        else:
            return False

    def defence_formation_save(self):
        if self.defence_formation_percent_check():
            message = "Formation updated successfully."
            positions = DefencePosition.objects.filter(user= self.user)
            for pos in positions:
                pos.user_troop = UserTroops.objects.get(id = int(self.data[f"troop{pos.position}"]))
                pos.percent = int(self.data[f"numd{pos.position}"])
                pos.save()
            return message
        else:
            message = "All troops' total percentage should be equal or lower then %100."
            return message
        
    def send_troop_number_check(self):
        filtered_data = {k:v for k,v in self.data.items() if k.startswith('troop')}
        new_data = dict.fromkeys(set(filtered_data.values()), 0)
        for k,v in filtered_data.items():
            if v in new_data.keys():
                new_data[v] += int(self.data["num"+k[-2:]])
        checks=[]
        for k,v in new_data.items():
            if self.user_troop_query.get(id = int(k)).count >= v:
                checks.append(True)
            else:
                checks.append(False)
        if all(checks):
            return True
        else:
            return False

    # returns two location obj. - main_location and target_location
    def main_and_target_locations(self):
        main_location = Location.objects.get(user=self.user)
        target_location = Location.objects.get(locx= int(self.data["locx"]), locy= int(self.data["locy"]))
        return main_location, target_location

    def send_troop(self):
        main_location, target_location = self.main_and_target_locations()
        if target_location.type == "nature":
            message = f"X:{target_location.locx} | Y:{target_location.locy} is not a place to send troop"
            return message
        else:
            # Create departing campaign object
            campaign = DepartingCampaigns.objects.create(
                user = self.user,
                main_location = main_location,
                target_location = target_location,
                campaign_type = self.data["sendType"],
                arriving_time = timezone.now()
            )

            # create departing troops
            for position in self.positions:
                user_troop = UserTroops.objects.get(id= self.data["troop"+str(position)])
                DepartingTroops.objects.create(
                    user= self.user,
                    position = position,
                    user_troop = user_troop,
                    count = int(self.data["num"+str(position)]),
                    campaign = campaign
                )
                user_troop.count -= int(self.data["num"+str(position)])
                user_troop.save()
            campaign.time_left = round(campaign.distance / campaign.speed * 3600)
            campaign.arriving_time = timezone.now() + timedelta(seconds=campaign.time_left)
            campaign.save()
            # send signal for tasks
            self.send_campaign_created_signal(campaign)
            message = f"Troops has left to {target_location.user}"
            return message


        

    def send_campaign_created_signal(self, campaign):
        campaign_created_signal.send(sender=None, instance=campaign)