from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from encampment.models import DepartingCampaigns
from .models import Battles
from .simulation import Battle

# TESTING VIEW

@login_required
def battle_view(request):
    departing_campaign = DepartingCampaigns.objects.get(id=111)
    battle = Battle(departing_campaign)
    if departing_campaign.campaign_type == "reinforcement":
        print("This is Reinforcement")
        pass
    elif departing_campaign.campaign_type == "attackblock":
        print("This is Block/line Battle")
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.block_battle_fight()

        battle.create_battle_report_objects()
        battle.arriving_create_and_resource_pillage()
        battle.delete_defender_dead_troops()
        # battle.delete_departing_campaign()

    elif departing_campaign.campaign_type == "attackflank":
        print("This is Flank Battle")
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.flank_battle_fight()

        battle.create_battle_report_objects()
        battle.arriving_create_and_resource_pillage()
        battle.delete_defender_dead_troops()
        # battle.delete_departing_campaign()
    elif departing_campaign.campaign_type == "pillage":
        print("This is pillage")
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.pillage_battle_fight()
        battle.create_battle_report_objects()
        battle.arriving_create_and_resource_pillage()
        battle.delete_defender_dead_troops()
        # battle.delete_departing_campaign()
    else:
        pass


    context = {
        "attack_group": attack_group,
        "defend_group": defend_group,
        "attacker_deads": attacker_deads,
        "defender_deads": defender_deads,
        "main_defend_group": main_defend_group,
        "main_attack_group": main_attack_group,

    }


    return render(request, "battle/battle.html", context)


class BattleReportDetailView(LoginRequiredMixin, DetailView):
    model = Battles
    template_name = "battle/report.html"
    context_object_name = "report"

# UTILS FUNCS


