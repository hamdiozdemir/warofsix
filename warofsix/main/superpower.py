from main.models import UserBuildings, SuperPower, SuperPowerReports, Race, UserTroops, Resources, UserTracker
import random
from django.utils import timezone
import math



class SuperPowerManagement():

    def __init__(self, user, user_fortress_id):
        self.user = user
        self.user_fortress = UserBuildings.objects.get(id = user_fortress_id)
        self.super_power = SuperPower.objects.get(user_building = self.user_fortress)


    def check_building_level(self):
        if self.user_fortress.level > 19:
            return True
        else:
            return False


    def check_reload_time(self):
        
        if self.super_power.is_active == False:
            return False, "You have not achived this yet."
        elif self.super_power.next_round != 0:
            return False, "Power is not loaded yet."
        else:
            return True, "ok"
    

    def send_attack(self, location):
        if self.check_building_level() and all(self.check_reload_time()):
            user_race = Race.objects.get(user=self.user).name
            # Updating the user's trainings etc send a signal by tracker
            if location.type == "settlement" and location.user:
                tracker = UserTracker.objects.get(user = location.user)
                tracker.track += 1
                tracker.save()
            elif location.type == "wild" and location.user:
                from .wild import WildUpdates
                wilder = WildUpdates(location.user)
                wilder.troop_update()
            # This races target the troops 
            if user_race in ["Elves", "Goblins", "Isengard"]:
                target_user_troops = UserTroops.objects.filter(user = location.user).exclude(count=0)
                # if there is no troop, create an empty one and reset the time
                if not target_user_troops.exists():
                    SuperPowerReports.objects.create(
                        super_power = self.super_power,
                        location = location,
                        troop = None
                    )
                    self.super_power.last_checkout = timezone.now()
                    self.super_power.save()
                    
                else:
                    attacked_troop = random.choice(target_user_troops)
                    troop_total_health = attacked_troop.count * attacked_troop.defence_level * attacked_troop.troop.health
                    damage_ratio = self.super_power.power_damage / troop_total_health
                    if damage_ratio > 1:
                        # kill all
                        SuperPowerReports.objects.create(
                            super_power = self.super_power,
                            location = location,
                            troop = attacked_troop.troop,
                            deads = attacked_troop.count
                        )
                        attacked_troop.count = 0
                        attacked_troop.save()
                    else:
                        dead_troops = math.ceil(attacked_troop.count * damage_ratio)
                        SuperPowerReports.objects.create(
                            super_power = self.super_power,
                            location = location,
                            troop = attacked_troop.troop,
                            deads = dead_troops                            
                        )
                        attacked_troop.count -= dead_troops
                        attacked_troop.save()
                    self.super_power.last_checkout = timezone.now()
                    self.super_power.save()
                return "Attack has sent. You may see the result in the reports."

            elif user_race == "Men":
                target_user_troops = UserTroops.objects.filter(user = location.user).exclude(count=0)
                # if there is no troop, create an empty one and reset the time
                if not target_user_troops.exists():
                    SuperPowerReports.objects.create(
                        super_power = self.super_power,
                        location = location,
                        revealed_troop = None
                    )
                    self.super_power.last_checkout = timezone.now()
                    self.super_power.save()
                else:
                    attacked_troop = random.choice(target_user_troops)
                    SuperPowerReports.objects.create(
                            super_power = self.super_power,
                            location = location,
                            revealed_troop = attacked_troop.troop,
                            revealed_count = attacked_troop.count,
                            revealed_attack_level = attacked_troop.attack_level,
                            revealed_defence_level = attacked_troop.defence_level
                            )

                    self.super_power.last_checkout = timezone.now()
                    self.super_power.save()
                return "Ivory Tower has seen. You may see the result in the reports."

            
            
            else:
                #buildingler için aynısı
                target_user_buildings = UserBuildings.objects.filter(user=location.user)
                if not target_user_buildings.exists():
                    SuperPowerReports.objects.create(
                        super_power = self.super_power,
                        location = location,
                    )
                    self.super_power.last_checkout = timezone.now()
                    self.super_power.save()
                else:
                    attacked_building = random.choice(target_user_buildings)
                    damage_ratio = self.super_power.power_damage / attacked_building.current_health
                    if damage_ratio > 1:
                        # demolish the building
                        SuperPowerReports.objects.create(
                            super_power = self.super_power,
                            location = location,
                            building = attacked_building.building,
                            pre_level = attacked_building.level,
                            post_level = 0
                        )
                        attacked_building.delete()
                    else:
                        post_level = math.floor(attacked_building.level * damage_ratio)
                        SuperPowerReports.objects.create(
                            super_power = self.super_power,
                            location = location,
                            building = attacked_building.building,
                            pre_level = attacked_building.level,
                            post_level = post_level
                        )
                        attacked_building.level = post_level
                        attacked_building.save()
                    self.super_power.last_checkout = timezone.now()
                    self.super_power.save()
                return "Attack has sent. You may see the result in the reports."

        else:
            return "Attack is not ready yet."


    def upgrade_super_power(self):
        user_resources = Resources.objects.get(user = self.user)

        if self.check_building_level() and all([
            user_resources.wood > 9999,
            user_resources.stone > 9999,
            user_resources.iron > 9999,
            user_resources.grain > 9999
        ]):
            user_resources.wood -= 10000
            user_resources.stone -= 10000
            user_resources.iron -= 10000
            user_resources.grain -= 10000
            user_resources.save()
            self.super_power.is_active = True
            self.super_power.save()
