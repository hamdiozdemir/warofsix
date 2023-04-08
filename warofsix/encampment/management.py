from main.models import UserTroops, Location, Resources, UserHeroes
from .models import DefencePosition, DepartingCampaigns, DepartingTroops, ArrivingCampaigns, ArrivingTroops, ReinforcementTroops, DepartingHeroes
from django.utils import timezone
from datetime import timedelta
from main.signals import departing_campaign_created_signal, current_resources



# When the task ready works, it sould check what the type of the departing troop, and then call the relevant funcs 

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
        
    def defence_formation_hero_check(self):
        filtered_data = {k:v for k,v in self.data.items() if k.startswith('herod') and v != "Add Hero"}
        if len(filtered_data.values()) == len(set(filtered_data.values())):
            return True, filtered_data
        else:
            return False, filtered_data



    def defence_formation_save(self):
        user_hero_check, filtered_hero_data = self.defence_formation_hero_check()
        if self.defence_formation_percent_check() and user_hero_check:
            message = "Formation updated successfully."
            positions = DefencePosition.objects.filter(user= self.user)
            for pos in positions:
                if pos.user_troop == UserTroops.objects.get(id = int(self.data[f"troop{pos.position}"])) and pos.percent == int(self.data[f"numd{pos.position}"]):
                    pass
                elif pos.user_troop == UserTroops.objects.get(id = int(self.data[f"troop{pos.position}"])) and pos.percent != int(self.data[f"numd{pos.position}"]):
                    pos.percent = int(self.data[f"numd{pos.position}"])
                    pos.save()
                else:
                    pos.user_troop = UserTroops.objects.get(id = int(self.data[f"troop{pos.position}"]))
                    pos.percent == int(self.data[f"numd{pos.position}"])
                    pos.save()
            for key, value in filtered_hero_data.items():
                if value == "Add Hero":
                    pass
                else:
                    user_hero = UserHeroes.objects.get(id = int(value))
                    user_hero.position = int(key[-2:])
                    user_hero.save()
            return message
        
        elif not user_hero_check:
            message = "You can use a hero only in one position"
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
        
    def send_troop_hero_check(self):
        filtered_data = {k:v for k,v in self.data.items() if k.startswith('herod') and v != "Add Hero"}
        if filtered_data == {}:
            return True, "OK"
        elif len(filtered_data.values()) != len(set(filtered_data.values())):
            message = "You can assign a hero to only one block!"
            return False, message
        else:
            user_hero_ids = [int(x) for x in filtered_data.values()]
            check = [UserHeroes.objects.get(id = id_data).is_available for id_data in user_hero_ids]
            print(check)
            if all(check):
                message = "OK"
                return True, message
            else:
                message = "One of the heroes is not available !"
                return False, message
                



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
        
        elif not self.send_troop_number_check():
            message = "You do not have enough troop!"
            return message
        elif not all(self.send_troop_hero_check()):
            check, message = self.send_troop_hero_check() 
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

            filtered_data = {int(k[-2:]):int(v) for k,v in self.data.items() if k.startswith('herod') and v != "Add Hero"}
            for pos, user_hero_id in filtered_data.items():
                DepartingHeroes.objects.create(
                    user = self.user,
                    position = pos,
                    user_hero = UserHeroes.objects.get(id = user_hero_id),
                    campaign = campaign
                )
            campaign.time_left = round(campaign.distance / campaign.speed * 3600)
            campaign.arriving_time = timezone.now() + timedelta(seconds=campaign.time_left)
            campaign.save()
            # send signal for tasks
            self.send_campaign_created_signal(campaign)
            message = f"Troops has left to {target_location.user}"
            return message


    def send_campaign_created_signal(self, campaign):
        departing_campaign_created_signal.send(sender=None, instance=campaign)



# Handle after the campaing return back

class Arrivings():

    def __init__(self, arriving_campaign):
        self.arriving_campaign = arriving_campaign
        self.user = arriving_campaign.user
        self.user_resources = Resources.objects.get(user = self.user)
        # self.user_troop = UserTroops.objects.filter(user= self.user)

    def handle_arriving(self):
        self.get_user_troops()
        self.get_resources()
        self.delete_arriving_campaign()

    def get_user_troops(self):
        arriving_group = self.arriving_campaign.group
        for obj in arriving_group:
            obj.user_troop.count += obj.count
            obj.user_troop.save()

    def get_user_heroes(self):
        arriving_heroes = self.arriving_campaign.heroes
        for obj in arriving_heroes:
            obj.user_hero.is_home = True
            obj.user_hero.save()

    def get_resources(self):
        # Update current resources
        current_resources(self.user)
        self.user_resources.wood += self.arriving_campaign.arriving_wood
        self.user_resources.stone += self.arriving_campaign.arriving_stone
        self.user_resources.iron += self.arriving_campaign.arriving_iron
        self.user_resources.grain += self.arriving_campaign.arriving_grain
        self.user_resources.save()

    def delete_arriving_campaign(self):
        self.arriving_campaign.delete()