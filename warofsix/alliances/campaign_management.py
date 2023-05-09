from datetime import timedelta
from main.models import UserTroops, UserHeroes
from encampment.management import TroopManagements
from .models import AllianceDepartingCampaign, AllianceDepartingHeroes, AllianceDepartingTroops
from encampment.models import DepartingCampaigns, DepartingTroops, DepartingHeroes
from django.utils import timezone



class AllianceCampaignManagement(TroopManagements):

    def __init__(self, data, user, alliance_member):
        self.data = data
        self.user = user
        self.user_troop_query = UserTroops.objects.filter(user=self.user)
        self.positions = [11,12,13,14,21,22,23,24,31,32,33,34]
       
        self.alliance_member = alliance_member
        self.alliance = alliance_member.alliance
        


    def my_func(self):
        return "MY FUNC"


    def create_alliance_campaign(self):
        main_location, target_location = self.main_and_target_locations()
   
        if target_location.type == "nature" or not target_location.user:
            message = f"X:{target_location.locx} | Y:{target_location.locy} is not a place to send troop"
            return message
        
        elif not self.send_troop_number_check():
            message = "You do not have enough troop !"
            return message
        
        elif not all(self.send_troop_hero_check()):
            check, message = self.send_troop_hero_check()
            return message
        
        else:
            # Create alliance campaign object
            campaign = AllianceDepartingCampaign.objects.create(
                alliance = self.alliance,
                creator_user = self.alliance_member,
                main_location = main_location,
                target_location = target_location,
                campaign_type = self.data["sendType"]
            )

            # Create Alliance Troops
            for position in self.positions:
                if int(self.data["num"+str(position)]) == 0:
                    user_troop = None
                else:
                    user_troop = UserTroops.objects.get(id = int(self.data["troop"+str(position)]))
                    user_troop.count -= int(self.data["num"+str(position)])
                    user_troop.save()
                AllianceDepartingTroops.objects.create(
                    position = position,
                    user_troop = user_troop,
                    count = int(self.data["num"+str(position)]),
                    campaign = campaign
                )
                # minus user_troop count. that troops will preserve
                

            #Crete hero objects
            hero_data = {int(k[-2:]):int(v) for k,v in self.data.items() if k.startswith('herod') and v != "Add Hero"}
            for pos, user_hero_id in hero_data.items():
                user_hero = UserHeroes.objects.get(id=user_hero_id)
                AllianceDepartingHeroes.objects.create(
                    position = pos,
                    user_hero = user_hero,
                    campaign = campaign
                )

                user_hero.is_home = False
                user_hero.save()
                
            campaign.time_left = round(campaign.distance / campaign.speed * 3600)
            campaign.arriving_time = timezone.now() + timedelta(seconds=campaign.time_left)
            campaign.save()

            message = f"A new campaign is created vs. {target_location.user}"

            return message


    def save_alliance_campaign(self, alliance_campaign):
        if not self.send_troop_number_check():
            return "You do not have enough troop !"

        elif not all(self.send_troop_hero_check()):
            return "One of your hero is not available !"
        
        else:
            for object in alliance_campaign.group:
                if object.user_troop:
                    pass
                else:
                    object_pos = object.position
                    if not self.data.get("num"+str(object_pos)):
                        pass
                    elif self.data["num"+str(object_pos)] == "0":
                        pass
                    else:
                        user_troop = UserTroops.objects.get(id = int(self.data["troop"+str(object_pos)]))
                        object.user_troop = user_troop
                        object.count = int(self.data["num"+str(object_pos)])
                        object.save()

                        user_troop.count -= int(self.data["num"+str(object_pos)])
                        user_troop.save()
                    




            # Get Hero
            hero_data = {int(k[-2:]):int(v) for k,v in self.data.items() if k.startswith('herod') and v != "Add Hero"}
            for pos, user_hero_id in hero_data.items():
                if alliance_campaign.heroes.filter(position = pos).exists():
                    pass
                else:
                    user_hero = UserHeroes.objects.get(id=user_hero_id)
                    AllianceDepartingHeroes.objects.create(
                        position = pos,
                        user_hero = user_hero,
                        campaign = alliance_campaign
                    )

                    user_hero.is_home = False
                    user_hero.save()

            return "Campaign is saved."


    def send_alliance_campaign(self, alliance_campaign):
        try:
            # create departing campaign
            campaign = DepartingCampaigns.objects.create(
                user = alliance_campaign.creator_user.member,
                main_location = alliance_campaign.main_location,
                target_location = alliance_campaign.target_location,
                time_left = alliance_campaign.time_left,
                arriving_time = timezone.now() + timedelta(seconds=alliance_campaign.time_left),
                campaign_type = alliance_campaign.campaign_type
            )
            # Gather departing troops for bulk_create
            departing_troop_save = []
            for object in alliance_campaign.group:
                departing_troop_save.append(
                    DepartingTroops(
                    user = object.user_troop.user if object.user_troop else object.campaign.creator_user.member,
                    position = object.position,
                    user_troop = object.user_troop,
                    count = object.count,
                    campaign = campaign
                    )
                )
            DepartingTroops.objects.bulk_create(departing_troop_save)
            # Gather departing heroes for bulk_create
            departing_heroes_save = []
            for object in alliance_campaign.heroes:
                departing_heroes_save.append(
                    DepartingHeroes(
                    user = object.user_hero.user,
                    user_hero = object.user_hero,
                    position = object.position,
                    campaign = campaign
                    )
                )
            DepartingHeroes.objects.bulk_create(departing_heroes_save)
            from battle.tasks import battle_task
            battle_task.apply_async(args=[campaign.id], countdown = campaign.time_left)
            
            
            return True
        except:
            return False



    def delete_alliance_campaign(self, alliance_campaign):
        alliance_campaign.delete()
        return "Alliance campaign has deleted."
    


    def cancel_campaign(self, alliance_campaign):
        group = alliance_campaign.group

        for obj in group:
            if not obj.user_troop:
                pass
            else:
                obj.user_troop.count += obj.count
                obj.user_troop.save()
        
        heroes = alliance_campaign.heroes
        for obj in heroes:
            obj.user_hero.is_home = True
            obj.user_hero.save()
        
        alliance_campaign.delete()


