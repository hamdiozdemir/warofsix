from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import shared_task
from encampment.models import DepartingCampaigns, ArrivingCampaigns
from .simulation import Battle

celery = Celery('tasks', broker="amqp://guest@localhost//")

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "warofsix.settings"


@shared_task
def battle_task(campaign_id):
    departing_campaign = DepartingCampaigns.objects.get(id=campaign_id)
    target_location = departing_campaign.target_location
    if target_location.race == "Wild":
        from main.wild import WildUpdates
        wild = WildUpdates(target_location.user)
        wild.combine_resource_troop_update()
    elif target_location.race in ["Men, Elves","Dwarves", "Mordor","Isengard","Goblins"]:
        from main.models import UserTracker
        tracker = UserTracker.objects.get(user=target_location.user)
        tracker.track += 1
        tracker.save()
    else:
        pass


    # UPDATE THE TARGET'S TROOP AND RESOURCES
    battle = Battle(departing_campaign)
    if departing_campaign.campaign_type == "reinforcement":
        pass
    elif departing_campaign.campaign_type == "attackblock":
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.block_battle_fight()

        arriving_obj = battle.arriving_create_and_resource_pillage()
        battle.create_battle_report_objects(arriving_obj)
        battle.delete_defender_dead_troops() 
        battle.delete_departing_campaign()

    elif departing_campaign.campaign_type == "attackflank":
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.flank_battle_fight()

        arriving_obj = battle.arriving_create_and_resource_pillage()
        battle.create_battle_report_objects(arriving_obj)
        battle.delete_defender_dead_troops()
        battle.delete_departing_campaign()
    elif departing_campaign.campaign_type == "pillage":
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.pillage_battle_fight()
        arriving_obj = battle.arriving_create_and_resource_pillage()
        battle.create_battle_report_objects(arriving_obj)
        battle.delete_defender_dead_troops()
        battle.delete_departing_campaign()
    else:
        pass



@shared_task
def arriving_task(arriving_campaign_id):
    arriving_camp = ArrivingCampaigns.objects.get(id = arriving_campaign_id)
    from encampment.management import Arrivings
    arriving = Arrivings(arriving_camp)
    arriving.handle_arriving()


@shared_task
def send_reinforcement_task(departing_campaign_id, arriving_campaign_id):
    departing_camp = DepartingCampaigns.objects.get(id = departing_campaign_id)
    arriving_camp = ArrivingCampaigns.objects.get(id = arriving_campaign_id)
    from encampment.management import Arrivings
    camp_manager = Arrivings(arriving_camp)
    camp_manager.get_reinforcement()
    departing_camp.delete()


@shared_task
def reinforcement_return(arriving_campaign_id):
    from encampment.management import Arrivings
    campaign = ArrivingCampaigns.objects.get(id = arriving_campaign_id)
    camp_manager = Arrivings(campaign)
    camp_manager.get_user_troops()
    camp_manager.delete_arriving_campaign()


@shared_task
def resource_send(market_sent_id):
    from main.models import MarketSent, Resources
    obj = MarketSent.objects.get(id = market_sent_id)
    target_resource = Resources.objects.get(user = obj.target_location.user)
    target_resource.wood += obj.wood
    target_resource.stone += obj.stone
    target_resource.iron += obj.iron
    target_resource.grain += obj.grain
    target_resource.save()
    obj.is_complete = True
    obj.save()
    