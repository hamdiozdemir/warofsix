from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from encampment.models import DepartingCampaigns
from .models import Battles
from .simulation import Battle



@login_required
def battle_view(request):
    departing_campaign = DepartingCampaigns.objects.get(id=64)
    battle = Battle(departing_campaign)
    attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.block_battle_fight()
    print(attack_group)
    print("*********************************************************")
    print(defend_group)
    battle.create_battle_report_objects()
    battle.arriving_create_and_resource_pillage()
    battle.delete_defender_dead_troops()


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

def attack_position_parser(queryset):
    positions = {
        11: [x for x in queryset.filter(position=11).exclude(count = 0)],
        12: [x for x in queryset.filter(position=12).exclude(count = 0)],
        13: [x for x in queryset.filter(position=13).exclude(count = 0)],
        14: [x for x in queryset.filter(position=14).exclude(count = 0)],
        21: [x for x in queryset.filter(position=21).exclude(count = 0)],
        22: [x for x in queryset.filter(position=22).exclude(count = 0)],
        23: [x for x in queryset.filter(position=23).exclude(count = 0)],
        24: [x for x in queryset.filter(position=24).exclude(count = 0)],
        31: [x for x in queryset.filter(position=31).exclude(count = 0)],
        32: [x for x in queryset.filter(position=32).exclude(count = 0)],
        33: [x for x in queryset.filter(position=33).exclude(count = 0)],
        34: [x for x in queryset.filter(position=34).exclude(count = 0)],
    }
    return positions

def defence_position_parser(queryset):
    positions = {
        11: [x for x in queryset.filter(position=11).exclude(percent = 0)],
        12: [x for x in queryset.filter(position=12).exclude(percent = 0)],
        13: [x for x in queryset.filter(position=13).exclude(percent = 0)],
        14: [x for x in queryset.filter(position=14).exclude(percent = 0)],
        21: [x for x in queryset.filter(position=21).exclude(percent = 0)],
        22: [x for x in queryset.filter(position=22).exclude(percent = 0)],
        23: [x for x in queryset.filter(position=23).exclude(percent = 0)],
        24: [x for x in queryset.filter(position=24).exclude(percent = 0)],
        31: [x for x in queryset.filter(position=31).exclude(percent = 0)],
        32: [x for x in queryset.filter(position=32).exclude(percent = 0)],
        33: [x for x in queryset.filter(position=33).exclude(percent = 0)],
        34: [x for x in queryset.filter(position=34).exclude(percent = 0)],
    }
    return positions

