from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from encampment.models import DefencePosition, DepartingCampaigns
from main.models import UserHeroes, UserBuildings, Statistic
from .models import Battles, AttackerDeads, DefenderDeads
from .simulation import Attacker, Defender, BlockBattle2
from django.db.models import Q
from django.contrib.auth.models import User
import math
from .simulation import block_matcher, block_calculations, block_battle_simulation_match, block_battle_simulation_not_equal_unmatch

# Create your views here.


@login_required
def battle_view(request):
    defender_user = User.objects.get(id=33)
    print(defender_user)
    attacker_user = User.objects.get(id=32)
    print(attacker_user)
    print("****************************************************************")

    # USER STATOSTIC OBJECTS
    attacker_statistic = Statistic.objects.get(user=32)
    defender_statistic = Statistic.objects.get(user=33)

    defender = DefencePosition.objects.filter(user=33)
    defender_heroes = UserHeroes.objects.filter(user=33)

    attacker = DepartingCampaigns.objects.get(id=24)
    attacker_heroes = UserHeroes.objects.filter(user=32)

    attack = Attacker(attacker.group, attacker_heroes)
    attack_group = attack.get_attack_troops()

    defend = Defender(defender, defender_heroes, user=33)
    defend_group = defend.get_defend_troops()
    defend_user = defend.get_defender_user()

    main_defend_group = defend.get_defend_troops()
    main_attack_group = attack.get_attack_troops()

    defender_deads = {
        11:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        12:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        13:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        14:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        21:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        22:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        23:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        24:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        31:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        32:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        33:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        34:{"user_troop":"", "deads":0, "hero_troop_deads": 0}
    }
    attacker_deads = {
        11:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        12:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        13:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        14:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        21:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        22:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        23:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        24:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        31:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        32:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        33:{"user_troop":"", "deads":0, "hero_troop_deads": 0},
        34:{"user_troop":"", "deads":0, "hero_troop_deads": 0}
    }

    
    war_end = False
    while not war_end:
        # MATCH OLANLARI BUL
        war_end, att_match, def_match, att_unmatch, def_unmatch = block_matcher(attack_group, defend_group)
        if war_end:
            print("SAVAŞ BİTTİ")
            break
        print("YENİ MATCH")
        print(f"WAR END: {war_end}")
        print(f"ATTACK MATCH: {att_match}")
        print(f"DEFEND MATCH: {def_match}")
        print(f"ATTACK UNMACTH: {att_unmatch}")
        print(f"DEFEND UNMATCH: {def_unmatch}")

        
        # YENİ DURUMA GÖRE HESAPLAMALARI YAP
        attack_group, defend_group = block_calculations(att_match, def_match, att_unmatch, def_unmatch, attack_group, defend_group)

        if att_unmatch != [] and def_unmatch != []:
            attack_group, defend_group, attacker_deads, defender_deads = block_battle_simulation_not_equal_unmatch(att_unmatch, def_unmatch, attack_group, defend_group, attacker_deads, defender_deads, attacker_statistic, defender_statistic)
            print("UNMATCH BATTLE ÇALIŞTI")

        elif att_unmatch == [] and def_unmatch != []:
            rest_temp_damage = 0
            for block in def_unmatch:
                rest_temp_damage += defend_group[block]["temp_defence_damage"]
            
            for block in def_match:
                defend_group[block]["temp_defence_damage"] += rest_temp_damage / len(def_match)
        elif att_unmatch != [] and def_unmatch == []:
            rest_temp_damage = 0
            for block in att_unmatch:
                rest_temp_damage += attack_group[block]["temp_attack_damage"]
            for block in att_match:
                attack_group[block]["temp_attack_damage"] += rest_temp_damage / len(att_match)
        else:
            pass

        # MATCHES BATTLE
        if att_match != []:
            attack_group, defend_group, attacker_deads, defender_deads = block_battle_simulation_match(att_match, def_match, attack_group, defend_group, attacker_deads, defender_deads, attacker_statistic, defender_statistic)
            print("MATCH BATTLE ÇALIŞTI")
        
    defendGrid = defence_position_parser(defender)
    attackGrid = attack_position_parser(attacker.group)

    blocks = [11,12,13,14,21,22,23,24,31,32,33,34]
    for block in blocks:
        try:
            if defender_deads[block]["deads"] == main_defend_group[block]["count"]:
                defender_deads[block].update({"status": "dead"})
            elif defender_deads[block]["deads"] != 0:
                defender_deads[block].update({"status": "injured"})
            else:
                defender_deads[block].update({"status": "ok"})
        except:
            defender_deads[block].update({"status": "dead"})

        try:
            if attacker_deads[block]["deads"] == main_attack_group[block]["count"]:
                attacker_deads[block].update({"status": "dead"})
            elif attacker_deads[block]["deads"] != 0:
                attacker_deads[block].update({"status": "injured"})
            else:
                attacker_deads[block].update({"status": "ok"})
        except:
            attacker_deads[block].update({"status": "dead"})

    battle = Battles.objects.create(attacker=attacker_user, defender=defender_user)
    for block in blocks:
        if main_attack_group.get(block):
            AttackerDeads.objects.create(
                battle=battle,
                user_troop = main_attack_group[block]["troop"] if main_attack_group[block].get("troop") else None,
                troop_count = main_attack_group[block]["count"],
                deads = attacker_deads[block]["deads"],
                position = block,
                status = attacker_deads[block]["status"],
                user_hero = main_attack_group[block]["hero"] if main_attack_group[block].get("hero") else None,
                user_hero_troop = main_attack_group[block]["hero_troop"] if main_attack_group[block].get("hero_troop") else None,
                user_hero_troop_count = main_attack_group[block]["hero_troop_count"] if main_attack_group[block].get("hero_troop_count") else 0,
                user_hero_troop_dead = attacker_deads[block]["hero_troop_deads"]
                
            )
        if main_defend_group.get(block):
            DefenderDeads.objects.create(
                battle=battle,
                user_troop = main_defend_group[block]["troop"] if main_defend_group[block].get("troop") else None,
                troop_count = main_defend_group[block]["count"],
                deads = defender_deads[block]["deads"],
                position = block,
                status = defender_deads[block]["status"],
                user_hero = main_defend_group[block]["hero"] if main_defend_group[block].get("hero") else None,
                user_hero_troop = main_defend_group[block]["hero_troop"] if main_defend_group[block].get("hero_troop") else None,
                user_hero_troop_count = main_defend_group[block]["hero_troop_count"] if main_defend_group[block].get("hero_troop_count") else 0,
                user_hero_troop_dead = defender_deads[block]["hero_troop_deads"]
            )

    
    context = {
        "defendGrid": defendGrid,
        "attackGrid": attackGrid,
        "defender": defender,
        "attacker": attacker,
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

