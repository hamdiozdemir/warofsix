from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from encampment.models import DefencePosition, DepartingCampaigns
from main.models import UserHeroes
from django.db.models import Q
import math

# Create your views here.


@login_required
def battle_view(request):
    defender = DefencePosition.objects.filter(user=33)
    defender_heroes = UserHeroes.objects.filter(user=33)
    # defence position'a location ekle. locationa göre filtrele. başka destek gönderenler de olabilir.
    # aynı şekilde attacker da birden fazla olabilir. ona göre filtrelenecek.
    attacker = DepartingCampaigns.objects.get(id=24)
    attacker_heroes = UserHeroes.objects.filter(user=32)

    attack = Attacker(attacker.group, attacker_heroes)
    attack_group = attack.get_attack_troops()

    defend = Defender(defender, defender_heroes)
    defend_group = defend.get_defend_troops()

    first_block = BlockBattle(attack_group, defend_group)
    first_result = first_block.first_block()
























    defendGrid = defence_position_parser(defender)
    attackGrid = attack_position_parser(attacker.group)

    # ROUND 1

    # round_1 = {
    #     11:{},
    #     12:{},
    #     13:{},
    #     14:{},
    #     15:{
    #     "att":[],
    #     "def":[]
    #     },
    #     "common":{},
    # }

    # # 1st Block
    # rows = [11,12,13,14]
    

    # battle_slot_num = 0
    # for cell in rows:
    #     if attackGrid[cell] != [] and defendGrid[cell] != []:
    #         battle_slot_num += 1
    #         attacker_attack = 0
    #         attacker_health = 0
    #         defender_attack = 0
    #         defender_health = 0

    #         for a, d in zip(attackGrid[cell], defendGrid[cell]):
    #             attacker_ratio = attack_ratio(a.user_troop, d.user_troop)
    #             defender_ratio = attack_ratio(d.user_troop, a.user_troop)

    #             attacker_attack += a.count * a.user_troop.troop.damage * a.user_troop.attack_level * attacker_ratio
    #             attacker_health_per_troop = a.user_troop.troop.health * a.user_troop.defence_level
    #             attacker_health += a.count * attacker_health_per_troop

    #             if d.user_troop.troop.crash_bonus != 0:
    #                 attacker_health -= d.count * d.user_troop.troop.crash_bonus
                

    #             for archer in attackGrid[cell+10]:
    #                 if archer.user_troop.troop.type == "archer":
    #                     archer_ratio = attack_ratio(archer.user_troop, d.user_troop)
    #                     attacker_attack += archer.count * archer.user_troop.troop.damage * archer_ratio
                
    #             defender_attack += d.count * d.user_troop.troop.damage * d.user_troop.attack_level * defender_ratio
    #             defender_health_per_troop = d.user_troop.troop.health * d.user_troop.defence_level
    #             defender_health += d.count * defender_health_per_troop
    #             if a.user_troop.troop.crash_bonus != 0:
    #                 defender_health -= a.count * a.user_troop.troop.crash_bonus
 
    #             for archer in defendGrid[cell+10]:
    #                 if archer.user_troop.troop.type == "archer":
    #                     archer_ratio = attack_ratio(archer.user_troop, a.user_troop)
    #                     defender_attack += archer.count * archer.user_troop.troop.damage * archer_ratio
    #         # results of the matching
    #         round_1[cell]["attacker_attack"] = attacker_attack
    #         round_1[cell]["attacker_health"] = attacker_health
    #         round_1[cell]["defender_attack"] = defender_attack
    #         round_1[cell]["defender_health"] = defender_health
    #         round_1[cell]["ahpt"] = attacker_health_per_troop
    #         round_1[cell]["dhpt"] = defender_health_per_troop
    #         round_1[cell]["attacker_user_troop"] = attackGrid[cell][0].user_troop
    #         round_1[cell]["defender_user_troop"] = defendGrid[cell][0].user_troop





    #     # pass if both sides are empty
    #     elif attackGrid[cell] == [] and defendGrid[cell] == []:
    #         pass
    #     # One size has troop, so get them to position 15 temprory
    #     else:
    #         round_1[15]["att"] = attackGrid[cell]
    #         round_1[15]["def"] = defendGrid[cell]
        
    #     # IF BOTH SIDES HAS EMPTY sLOTS IN DIFFERENT COLUMN, match them without ratio and let them fight in pos COMMON, not effecting by ratio or archers'        
    #     if round_1[15]["att"] != [] and round_1[15]["def"] != []:
    #         attacker_attack15 = 0
    #         attacker_health15 = 0
    #         defender_attack15 = 0
    #         defender_health15 = 0
    #         for att in round_1[15]["att"]:
    #             attacker_attack15 += att.count * att.user_troop.attack_level * att.user_troop.troop.damage
    #             attacker_health15 += att.count * att.user_troop.defence_level * att.user_troop.troop.health
    #         for deff in round_1[15]["def"]:
    #             defender_attack15 += deff.count * deff.user_troop.attack_level * deff.user_troop.troop.damage
    #             defender_health15 += deff.count * deff.user_troop.attack_level * deff.user_troop.troop.health
    #         round_1["common"] = {
    #             "attacker_attack15": attacker_attack15,
    #             "attacker_health15": attacker_health15,
    #             "defender_attack15": defender_attack15,
    #             "defender_health15":defender_health15
    #         }

    #     # IF ONLY ONE SIDE HAS TROOP, DIVIDE THEIR ATTACK TO OTHERS'
    #     elif round_1[15]["att"] != []:
    #         attacker_attack15 = 0
    #         troop_size = 0
    #         for att in round_1[15]["att"]:
    #             attacker_attack15 += att.count * att.user_troop.attack_level * att.user_troop.troop.damage
    #             troop_size += att.count
    #         round_1["common"] = {
    #             "attacker_attack15": attacker_attack15,
    #         }
    #         att_per_slot = attacker_attack15 / battle_slot_num
    #         for cell in rows:
    #             if round_1[cell] != {}:
    #                 round_1[cell]["attacker_attack"] += att_per_slot
            
    #     elif round_1[15]["def"] != []:
    #         defender_attack15 = 0
    #         troop_size = 0
    #         for deff in round_1[15]["def"]:
    #             defender_attack15 += deff.count * deff.user_troop.attack_level * deff.user_troop.troop.damage
    #             troop_size += deff.count
    #         att_per_slot = defender_attack15 / battle_slot_num
    #         for cell in rows:
    #             if round_1[cell] != {}:
    #                 round_1[cell]["defender_attack"] += att_per_slot
    #     else:
    #         pass


    # round_2 = {
    #     "att": {},
    #     "def":{}
    # }
    # battle_rows = [11,12,13,14,"common"]
    # for cell in battle_rows:
    #     # print(round_1[cell].values())
    #     if len(round_1[cell].keys()) == 0:
    #         pass
    #     else:
    #         a_d_ratio = round_1[cell].get("attacker_attack") / round_1[cell].get("defender_health")
    #         # print(a_d_ratio)
    #         d_a_ratio = round_1[cell].get("defender_attack") / round_1[cell].get("attacker_health")
    #         if a_d_ratio > d_a_ratio:
    #             print(f"ATTACKER WINS in position {cell}")
    #             round_1[cell]["defender_deads"] = round_1[cell]["defender_health"] / round_1[cell]["dhpt"]

    #             round_1[cell]["attacker_deads"] = math.floor(round_1[cell]["defender_attack"] / a_d_ratio / round_1[cell]["ahpt"])
    #         elif d_a_ratio > a_d_ratio:
    #             print(f"DEFENDER WINS in position {cell}")
    #             round_1[cell]["attacker_deads"] = round_1[cell]["attacker_health"] / round_1[cell]["ahpt"]

    #             round_1[cell]["defender_deads"] = math.floor(round_1[cell]["attacker_attack"] / d_a_ratio / round_1[cell]["dhpt"])
    #         # print(round_1[cell])

    # print(round_1)
    uzunluk = len(attackGrid[11])
    context = {
        "defendGrid": defendGrid,
        "attackGrid": attackGrid,
        "defender": defender,
        "attacker": attacker,
        "uzunluk": uzunluk,
        "attack_group": attack_group,
        "defend_group": defend_group,
        "first_result": first_result
    }

    # context["round_1"] = round_1
    return render(request, "battle/battle.html", context)


# NOT REQUIRED RIGHT NOW
class BlockBattle():
    
    def __init__(self, attack_group, defend_group):
        self.attack_group = attack_group
        self.defend_group = defend_group

    
    def first_block(self):
        blocks = [11,12,13,14]
        first_battle_field={
            11:{
            "att":{},
            "def":{}
            },
            12:{
            "att":{},
            "def":{}
            },
            13:{
            "att":{},
            "def":{}
            },
            14:{
            "att":{},
            "def":{}
            },
            15:{
            "att":{},
            "def":{}
            }
        }
        match_number = 0
        attack_unmatch = []
        defend_unmatch = []
        for block in blocks:
            # if the both sides have troops in block
            if self.attack_group.get(block) and self.defend_group.get(block):
                match_number += 1
                att_troop = self.attack_group[block]["troop"]
                def_troop = self.defend_group[block]["troop"]
                #check if the block has a hero
                if self.attack_group[block].get("hero"):
                    hero_att_bonus = hero_attack_bonus(self.attack_group[block]["hero"], att_troop.user_troop)
                    hero_def_bonus = hero_defence_bonus(self.attack_group[block]["hero"], att_troop.user_troop)
                    hero_damage = self.attack_group[block]["hero"].hero.damage
                    hero_health = self.attack_group[block]["hero"].current_health
                else:
                    hero_att_bonus = 1
                    hero_def_bonus = 1
                    hero_damage = 0
                    hero_health = 0
                # attacker stats
                att_ratio = attack_ratio(att_troop.user_troop, def_troop.user_troop)
                att_damage = att_troop.count * att_ratio * att_troop.user_troop.troop.damage * att_troop.user_troop.attack_level * hero_att_bonus + hero_damage
                att_health = att_troop.count * att_troop.user_troop.troop.health * att_troop.user_troop.defence_level * hero_def_bonus + hero_health

                #check if archer behind -- aatacker
                if self.attack_group.get(block+10) and self.attack_group[block+10]["troop"].user_troop.troop.type == "archer":
                    if self.attack_group[block+10].get("hero"):
                        hero_bonus = hero_attack_bonus(self.attack_group[block+10]["hero"], self.attack_group[block+10]["troop"].user_troop)
                    else:
                        hero_bonus = 1
                    archer_damage = self.attack_group[block+10]["troop"].count * self.attack_group[block+10]["troop"].user_troop.troop.damage * self.attack_group[block+10]["troop"].user_troop.attack_level * hero_bonus
                    att_damage += archer_damage

                #defender stats
                if self.defend_group[block].get("hero"):
                    hero_att_bonus = hero_attack_bonus(self.defend_group[block]["hero"], def_troop.user_troop)
                    hero_def_bonus = hero_defence_bonus(self.defend_group[block]["hero"], def_troop.user_troop)
                    hero_damage = self.defend_group[block]["hero"].hero.damage
                    hero_health = self.defend_group[block]["hero"].current_health
                else:
                    hero_att_bonus = 1
                    hero_def_bonus = 1
                    hero_damage = 0
                    hero_health = 0
                att_ratio = attack_ratio(def_troop.user_troop, att_troop.user_troop)
                def_damage = def_troop.count * att_ratio * def_troop.user_troop.troop.damage * def_troop.user_troop.attack_level * hero_att_bonus + hero_damage
                def_health = def_troop.count * def_troop.user_troop.troop.health * def_troop.user_troop.defence_level * hero_def_bonus + hero_health

                #check if archer behind -- defender
                if self.defend_group.get(block+10) and self.defend_group[block+10]["troop"].user_troop.troop.type == "archer":
                    if self.defend_group[block+10].get("hero"):
                        hero_bonus = hero_attack_bonus(self.defend_group[block+10]["hero"], self.defend_group[block+10]["troop"].user_troop)
                    else:
                        hero_bonus = 1
                    archer_damage = self.defend_group[block+10]["troop"].count * self.defend_group[block+10]["troop"].user_troop.troop.damage * self.defend_group[block+10]["troop"].user_troop.attack_level * hero_bonus
                    def_damage += archer_damage


                first_battle_field[block]["att"] = {"troop": att_troop.user_troop, "attack_damage": att_damage, "attack_health": att_health}
                first_battle_field[block]["def"] = {"troop": def_troop.user_troop, "defence_damage": def_damage, "defence_health": def_health}

            # if block has only attacker
            elif self.attack_group.get(block):
                att_troop = self.attack_group[block]["troop"]

                if self.attack_group[block].get("hero"):
                    hero_att_bonus = hero_attack_bonus(self.attack_group[block]["hero"], att_troop.user_troop)
                    hero_def_bonus = hero_defence_bonus(self.atta_group[block]["hero"], att_troop.user_troop)
                else:
                    hero_att_bonus = 1
                    hero_def_bonus = 1


                att_damage = att_troop.count * att_troop.user_troop.troop.damage * att_troop.user_troop.attack_level * hero_att_bonus
                att_health = att_troop.count * att_troop.user_troop.troop.health * att_troop.user_troop.defence_level * hero_def_bonus
                first_battle_field[block]["att"] = {"troop":att_troop.user_troop, "attack_damage": att_damage, "attack_health": att_health}
                # add to unmatch
                attack_unmatch.append(block)

            # if block has only defender
            elif self.defend_group.get(block):
                if self.defend_group[block].get("hero"):
                    hero_att_bonus = hero_attack_bonus(self.defend_group[block]["hero"], def_troop.user_troop)
                    hero_def_bonus = hero_defence_bonus(self.defend_group[block]["hero"], def_troop.user_troop)
                else:
                    hero_att_bonus = 1
                    hero_def_bonus = 1

                
                def_damage = def_troop.count * def_troop.user_troop.troop.damage * def_troop.user_troop.attack_level * hero_att_bonus
                def_health = def_troop.count * def_troop.user_troop.troop.health * def_troop.user_troop.defence_level * hero_def_bonus
                first_battle_field[block]["deff"] = {"troop": def_troop.user_troop, "defence_damage": def_damage, "defence_health": def_health}
                # add to unmatch
                defend_unmatch.append(block)

            # both sides have no troop in block    
            else:
                pass

        print(f"ATAK UN MATCH: {attack_unmatch}")
        print(f"DEFANS UN MATCH: {defend_unmatch}")
        # BİREBİR EŞLEŞME OLURSA KULLANABİLİRİZ.
        if len(attack_unmatch) == 1 and len(defend_unmatch) == 1:
            print(f"BU BİR EŞLEŞME: {attack_unmatch[0]} ve {defend_unmatch[0]}")
        return first_battle_field
                
                

        

class Attacker():

    def __init__(self, attack_group, user_heroes):
        self.attack_group = attack_group
        self.user_heroes = user_heroes
    
    def get_attack_troops(self):
        positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        group = {}
        for pos in positions:
            if self.attack_group.filter(position=pos).exclude(count=0).exists():
                group[pos] = {"troop": self.attack_group.get(position=pos)}
            if self.user_heroes.filter(position=pos).exclude(is_dead=True).exists():
                if pos not in group:
                    group[pos] = {"hero": self.user_heroes.get(position=pos)}
                else:
                    group[pos].update({"hero": self.user_heroes.get(position=pos)})
        return group


class Defender():

    def __init__(self, defender_group, user_heroes):
        self.defender_group = defender_group
        self.user_heroes = user_heroes

    def get_defend_troops(self):
        positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        group = {}
        for pos in positions:
            if self.defender_group.filter(position=pos).exclude(percent=0).exists():
                group[pos] = {"troop": self.defender_group.get(position=pos)}
            if self.user_heroes.filter(position=pos).exclude(is_dead=True).exists():
                if pos not in group:
                    group[pos] = {"hero": self.user_heroes.get(position=pos)}
                else:
                    group[pos].update({"hero": self.user_heroes.get(position=pos)})
        return group






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


# UTILS FUNCS

def attack_ratio(user_troop_attacker, user_troop_defender):
    ratio = {
        "infantrypike": 1.4,
        "infantryarcher": 1.2,
        "infantrycavalry": 0.8,
        "archerinfantry": 0.8,
        "archerpike": 0.8,
        "archercavalry": 0.6,
        "pikeinfantry": 0.8,
        "pikecavalry": 1.5,
        "cavalryinfantry": 1.2,
        "cavalrypike": 0.6,
        "cavalryarcher": 1.8,
        "infantrymonster": 0.8,
        "pikemonster": 1.3,
        "archermonster": 1.2,
        "monsterinfantry": 1.3,
        "monsterarcher": 1.2,
    }
    compete = user_troop_attacker.troop.type + user_troop_defender.troop.type
    if compete in ratio.keys():
        return ratio[compete]
    else:
        return 1
    

def hero_attack_bonus(user_hero, user_troop):
    troop_type = user_troop.troop.type
    if troop_type == "infantry":
        return user_hero.hero.infantry_attack_bonus
    elif troop_type == "pike":
        return user_hero.hero.pike_attack_bonus
    elif troop_type == "cavalry":
        return user_hero.hero.cavalry_attack_bonus
    elif troop_type == "archer":
        return user_hero.hero.archer_attack_bonus
    elif troop_type == "monster":
        return user_hero.hero.monster_attack_bonus
    else:
        return 1

def hero_defence_bonus(user_hero, user_troop):
    troop_type = user_troop.troop.type
    if troop_type == "infantry":
        return user_hero.hero.infantry_defence_bonus
    elif troop_type == "pike":
        return user_hero.hero.pike_defence_bonus
    elif troop_type == "cavalry":
        return user_hero.hero.cavalry_defence_bonus
    elif troop_type == "archer":
        return user_hero.hero.archer_defence_bonus
    elif troop_type == "monster":
        return user_hero.hero.monster_defence_bonus
    else:
        return 1


