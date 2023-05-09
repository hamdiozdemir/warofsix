from encampment.models import DefencePosition, DepartingTroops, ArrivingCampaigns, ArrivingTroops, ReinforcementTroops, ArrivingHeroes
from main.models import UserHeroes, UserBuildings, Statistic, UserTroops, Resources
from .models import Battles, AttackerDeads, DefenderDeads, DefenderBuildingDemolish, BattlePillageResources
import math
from django.utils import timezone
from datetime import timedelta



class Attacker():

    def __init__(self, attack_group, campaign_heroes):
        self.attack_group = attack_group
        self.campaign_heroes = campaign_heroes
    
    def get_attack_troops(self):
        positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        group = {}
        for pos in positions:
            # If there are both TROOP and HERO
            if self.attack_group.filter(position=pos).exclude(count=0).exists() and self.campaign_heroes.filter(position = pos).exists():
                block_troop = self.attack_group.get(position=pos)
                user_troop = block_troop.user_troop
                group[pos] = {"troop": user_troop}
                hero = self.campaign_heroes.get(position=pos).user_hero
                group[pos].update({"hero": hero})
                hero_att_bonus = hero_attack_bonus(hero, user_troop)
                hero_def_bonus = hero_defence_bonus(hero, user_troop)
                if hero.hero.summon_amount != 0:
                    hero_damage = hero.hero.damage + hero.hero.crash_bonus + hero.hero.summon_amount * hero.hero.summon_type.damage
                    hero_health = hero.current_health + hero.hero.summon_amount * hero.hero.summon_type.health
                    group[pos].update({"hero_troop": hero.hero.summon_type, "hero_troop_count": hero.hero.summon_amount})
                else:
                    hero_damage = hero.hero.damage + hero.hero.crash_bonus
                    hero_health = hero.current_health 

                group[pos].update({"health_per_troop": user_troop.troop.health * user_troop.defence_level * hero_def_bonus})
                group[pos].update({"total_attack_health": block_troop.count * user_troop.troop.health * user_troop.defence_level * hero_def_bonus + hero_health})
                group[pos].update({"total_attack_damage": block_troop.count * user_troop.troop.damage * user_troop.attack_level * hero_att_bonus + hero_damage})
                group[pos].update({"count": block_troop.count})

            # IF only TROOP
            elif self.attack_group.filter(position=pos).exclude(count=0).exists():
                block_troop = self.attack_group.get(position=pos) 
                user_troop = block_troop.user_troop
                group[pos] = {"troop": user_troop}

                group[pos].update({"health_per_troop": user_troop.troop.health * user_troop.defence_level})
                group[pos].update({"total_attack_health": block_troop.count * user_troop.troop.health * user_troop.defence_level})
                group[pos].update({"total_attack_damage": block_troop.count * user_troop.troop.damage * user_troop.attack_level})
                group[pos].update({"count": block_troop.count})

            # IF only HERO
            elif self.campaign_heroes.filter(position=pos).exists():
                hero = self.campaign_heroes.get(position=pos).user_hero
                group[pos] = {"hero": hero}
                if hero.hero.summon_amount != 0:
                    hero_damage = hero.hero.damage + hero.hero.crash_bonus + hero.hero.summon_amount * hero.hero.summon_type.damage
                    hero_health = hero.current_health + hero.hero.summon_amount * hero.hero.summon_type.health
                    group[pos].update({"hero_troop": hero.hero.summon_type, "hero_troop_count": hero.hero.summon_amount})
                else:
                    hero_damage = hero.hero.damage + hero.hero.crash_bonus
                    hero_health = hero.current_health 

                group[pos].update({"total_attack_health": hero_health})
                group[pos].update({"health_per_troop": hero_health})
                group[pos].update({"total_attack_damage": hero_damage})
                group[pos].update({"count": 0})
            
            else:
                pass
        return group
    

class Defender():

    def __init__(self, defender_group, user_heroes):
        self.defender_group = defender_group
        self.user_heroes = user_heroes

    def get_defend_troops(self):
        positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        group = {}
        for pos in positions:
            # IF there are both TROOP and HERO
            troop_exists = self.defender_group.get(position = pos).count
            troop_exists = True if troop_exists > 0 else False
            if troop_exists and self.user_heroes.filter(position=pos).exists():
                block_troop = self.defender_group.get(position=pos)
                if block_troop.count < 1:
                    pass
                else:
                    user_troop = block_troop.user_troop
                    hero = self.user_heroes.get(position=pos)

                    group[pos] = {"troop": user_troop}
                    group[pos].update({"hero": hero})
                    hero_att_bonus = hero_attack_bonus(hero, user_troop)
                    hero_def_bonus = hero_defence_bonus(hero, user_troop)
                    if hero.hero.summon_amount != 0:
                        hero_damage = hero.hero.damage + hero.hero.crash_bonus + hero.hero.summon_amount * hero.hero.summon_type.damage
                        hero_health = hero.current_health + hero.hero.summon_amount * hero.hero.summon_type.health
                        group[pos].update({"hero_troop": hero.hero.summon_type, "hero_troop_count": hero.hero.summon_amount})
                    else:
                        hero_damage = hero.hero.damage + hero.hero.crash_bonus
                        hero_health = hero.current_health 


                    group[pos].update({"health_per_troop": user_troop.troop.health * user_troop.defence_level * hero_def_bonus})
                    group[pos].update({"total_defence_health": block_troop.count * user_troop.troop.health * user_troop.defence_level * hero_def_bonus + hero_health})
                    group[pos].update({"total_defence_damage": block_troop.count * user_troop.troop.damage * user_troop.attack_level * hero_att_bonus + hero_damage})
                    group[pos].update({"count": block_troop.count})

            elif troop_exists:
                block_troop = self.defender_group.get(position=pos)
                if block_troop.count < 1:
                    pass
                else:
                    user_troop = block_troop.user_troop
                    group[pos] = {"troop": user_troop}
                    group[pos].update({"health_per_troop": user_troop.troop.health * user_troop.defence_level})
                    group[pos].update({"total_defence_health": block_troop.count * user_troop.troop.health * user_troop.defence_level})
                    group[pos].update({"total_defence_damage": block_troop.count * user_troop.troop.damage * user_troop.attack_level})
                    group[pos].update({"count": block_troop.count})

            elif self.user_heroes.filter(position=pos).exists():
                hero = self.user_heroes.get(position=pos)
                group[pos] = {"hero": hero}

                if hero.hero.summon_amount != 0:
                    hero_damage = hero.hero.damage + hero.hero.crash_bonus + hero.hero.summon_amount * hero.hero.summon_type.damage
                    hero_health = hero.current_health + hero.hero.summon_amount * hero.hero.summon_type.health
                    group[pos].update({"hero_troop": hero.hero.summon_type, "hero_troop_count": hero.hero.summon_amount})
                else:
                    hero_damage = hero.hero.damage + hero.hero.crash_bonus
                    hero_health = hero.current_health 

                group[pos].update({"total_defence_health": hero_health})
                group[pos].update({"health_per_troop": hero_health})
                group[pos].update({"total_defence_damage": hero_damage})
                group[pos].update({"count": 1})
            
            else:
                pass
        return group


class Battle():

    def __init__(self, departing_campaign):
        self.departing_campaign = departing_campaign
        self.attacker_user = self.departing_campaign.user
        self.defender_user = self.departing_campaign.target_location.user
        self.attacker_statistic = Statistic.objects.get(user=self.attacker_user)
        self.defender_statistic = Statistic.objects.get(user=self.defender_user)
        self.blocks = [11,12,13,14,21,22,23,24,31,32,33,34]

        self.attacker_heroes = self.departing_campaign.heroes
        attack_obj = Attacker(self.departing_campaign.group, self.attacker_heroes)

        self.defender = DefencePosition.objects.filter(user=self.defender_user)
        self.defender_heroes = UserHeroes.objects.filter(user=self.defender_user, is_dead=False, is_home=True)
        defend_obj = Defender(self.defender, self.defender_heroes)

        self.attack_group = attack_obj.get_attack_troops()
        self.defend_group = defend_obj.get_defend_troops()

        self.main_attack_group = attack_obj.get_attack_troops()
        self.main_defend_group = defend_obj.get_defend_troops()

        self.defender_deads = {
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

        self.attacker_deads = {
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

    # MATCHING THE BLOCKS FOR BATTLE
    def block_battle_matcher(self):
        att_first = [x for x in self.attack_group.keys() if 10 < x < 15]
        att_second = [x for x in self.attack_group.keys() if 20 < x < 25]
        att_third = [x for x in self.attack_group.keys() if 30 < x < 35]
        def_first = [x for x in self.defend_group.keys() if 10 < x < 15]
        def_second = [x for x in self.defend_group.keys() if 20 < x < 25]
        def_third = [x for x in self.defend_group.keys() if 30 < x < 35]
        war_end = False
        if att_first != []:
            if def_first != []:
                common = list(set(att_first) & set(def_first))
                att_match = common
                def_match = common
                att_unmatch = [x for x in att_first if x not in common]
                def_unmatch = [x for x in def_first if x not in common]
            elif def_second != []:
                temp_def = [x-10 for x in def_second]
                common = list(set(att_first) & set(temp_def))
                att_match = common
                def_match = [x+10 for x in common]
                att_unmatch = [x for x in att_first if x not in att_match]
                def_unmatch = [x for x in def_second if x not in def_match]
            elif def_third != []:
                temp_def = [x-20 for x in def_third]
                common = list(set(att_first) & set(temp_def))
                att_match = common
                def_match = [x+20 for x in common]
                att_unmatch = [x for x in att_first if x not in att_match]
                def_unmatch = [x for x in def_third if x not in def_match]
            else:
                war_end = True
        elif att_second != []:
            if def_first != []:
                temp_def = [x+10 for x in def_first]
                common = list(set(att_second) & set(temp_def))
                att_match = common
                def_match = [x-10 for x in common]
                att_unmatch = [x for x in att_second if x not in att_match]
                def_unmatch = [x for x in def_first if x not in def_match]
            elif def_second != []:
                common = list(set(att_second) & set(def_second))
                att_match = common
                def_match = common
                att_unmatch = [x for x in att_second if x not in common]
                def_unmatch = [x for x in def_second if x not in common]
            elif def_third != []:
                # 2 vs 3
                temp_def = [x-10 for x in def_third]
                common = list(set(att_second) & set(temp_def))
                att_match = common
                def_match = [x+10 for x in common]
                att_unmatch = [x for x in att_second if x not in att_match]
                def_unmatch = [x for x in def_third if x not in def_match]
            else:
                war_end = True
        elif att_third != []:
            if def_first != []:
                # 3 vs 1
                temp_def = [x+20 for x in def_first]
                common = list(set(att_third) & set(temp_def))
                att_match = common
                def_match = [x-20 for x in common]
                att_unmatch = [x for x in att_third if x not in att_match]
                def_unmatch = [x for x in def_first if x not in def_match]
            elif def_second != []:
                # 3 vs 2
                temp_def = [x+10 for x in def_second]
                common = list(set(att_third) & set(temp_def))
                att_match = common
                def_match = [x-10 for x in common]
                att_unmatch = [x for x in att_third if x not in att_match]
                def_unmatch = [x for x in def_second if x not in def_match]
            elif def_third != []:
                # 3 vs 3
                common = list(set(att_third) & set(def_third))
                att_match = common
                def_match = common
                att_unmatch = [x for x in att_third if x not in common]
                def_unmatch = [x for x in def_third if x not in common]
            else:
                war_end = True

        else:
            war_end = True
        try:
            if len(att_unmatch) == len(def_unmatch):
                att_match = att_match + att_unmatch
                def_match = def_match + def_unmatch
                att_unmatch = []
                def_unmatch = []
        except:
            att_match = []
            def_match = []
            att_unmatch = []
            def_unmatch = []
        return war_end, att_match, def_match, att_unmatch, def_unmatch


    def block_calculations(self, attack_match, defend_match, attack_unmatched, defend_unmatched):
        # Get defensive buildings' damages (tower, warg sentry)
        defender_building_damage = self.defensive_building_damages()
        
        if attack_match != []:
            for aum, dum in zip(attack_match, defend_match):
                # Attack stats update
                if self.attack_group[aum].get("troop") and self.defend_group[dum].get("troop"):
                    att_ratio = attack_ratio(self.attack_group[aum]["troop"], self.defend_group[dum]["troop"])
                else:
                    att_ratio = 1
                troop_crash_bonus = self.attack_group[aum]["troop"].troop.crash_bonus * self.attack_group[aum]["count"] if self.attack_group[aum].get("troop") else 0
                self.attack_group[aum].update({"temp_attack_damage": self.attack_group[aum]["total_attack_damage"] * att_ratio + troop_crash_bonus})
                if self.attack_group[aum].get("hero"):
                    hero_crash_bonus = self.attack_group[aum]["hero"].hero.crash_bonus
                    self.attack_group[aum]["temp_attack_damage"] += hero_crash_bonus
                # Check if archer/siege behind
                try:
                    if self.attack_group[aum+10]["troop"].troop.type == "archer" or self.attack_group[aum+10]["troop"].troop.type == "siege":
                        if self.attack_group[aum+10].get("hero"):
                            hero_bonus = hero_attack_bonus(self.attack_group[aum+10]["hero"], self.attack_group[aum+10]["troop"])
                        else:
                            hero_bonus = 1
                        att_ratio = attack_ratio(self.attack_group[aum+10]["troop"], self.defend_group[dum]["troop"])
                        behind_damage = self.attack_group[aum+10]["count"] * self.attack_group[aum+10].attack_level * self.attack_group[aum+10]["troop"].troop.damage * hero_bonus * att_ratio
                        self.attack_group[aum]["temp_attack_damage"] += behind_damage
                except:
                    pass
                # Defender stats update
                if self.attack_group[aum].get("troop") and self.defend_group[dum].get("troop"):
                    att_ratio = attack_ratio(self.defend_group[dum]["troop"], self.attack_group[aum]["troop"])
                else:
                    att_ratio = 1
                troop_crash_bonus = self.defend_group[dum]["troop"].troop.crash_bonus * self.defend_group[dum]["count"] if self.defend_group[dum].get("troop") else 0

                self.defend_group[dum].update({"temp_defence_damage": self.defend_group[dum]["total_defence_damage"] * att_ratio + troop_crash_bonus + (defender_building_damage / 4)})
                # Check if archer/siege behind
                try:
                    dum10 = self.defend_group[dum+10]
                    if dum10["troop"].troop.type == "archer" or dum10["troop"].troop.type == "siege":
                        if dum10.get("hero"):
                            hero_bonus = hero_attack_bonus(dum10["hero"], dum10["troop"])
                        else:
                            hero_bonus = 1
                        att_ratio = attack_ratio(dum10["troop"], self.attack_group[aum]["troop"])
                        behind_damage = dum10["count"] * dum10["troop"].attack_level * dum10["troop"].troop.damage * hero_bonus * att_ratio
                        self.defend_group[dum]["temp_defence_damage"] += behind_damage
                except:
                    pass
        # Attack stats update
        if attack_unmatched != []:
            for aum in attack_unmatched:
                troop_crash_bonus = self.attack_group[aum]["troop"].troop.crash_bonus * self.attack_group[aum]["count"] if self.attack_group[aum].get("troop") else 0
                self.attack_group[aum].update({"temp_attack_damage": self.attack_group[aum]["total_attack_damage"] + troop_crash_bonus})
                # Check if archer/siege behind
                try:
                    if self.attack_group[aum+10]["troop"].troop.type == "archer" or self.attack_group[aum+10]["troop"].troop.type == "siege":
                        if self.attack_group[aum+10].get("hero"):
                            hero_bonus = hero_attack_bonus(self.attack_group[aum+10]["hero"], self.attack_group[aum+10]["troop"])
                        else:
                            hero_bonus = 1
                        behind_damage = self.attack_group[aum+10]["count"] * self.attack_group[aum+10].attack_level * self.attack_group[aum+10]["troop"].troop.damage * hero_bonus
                        self.attack_group[aum]["temp_attack_damage"] += behind_damage
                except:
                    pass
        # defend stats update
        if defend_unmatched != []:
            for dum in defend_unmatched:
                troop_crash_bonus = self.defend_group[dum]["troop"].troop.crash_bonus * self.defend_group[dum]["count"] if self.defend_group[dum].get("troop") else 0

                temp_defence_damage = self.defend_group[dum]["total_defence_damage"] + troop_crash_bonus + (defender_building_damage / 4)

                self.defend_group[dum].update({"temp_defence_damage": temp_defence_damage})
                # Check if archer/siege behind
                try:
                    dum10 = self.defend_group[dum+10]
                    if dum10["troop"].troop.type == "archer" or dum10["troop"].troop.type == "siege":
                        if dum10.get("hero"):
                            hero_bonus = hero_attack_bonus(dum10["hero"], dum10["troop"])
                        else:
                            hero_bonus = 1
                        behind_damage = dum10["count"] * dum10["troop"].attack_level * dum10["troop"].troop.damage * hero_bonus
                        self.defend_group[dum]["temp_defence_damage"] += behind_damage
                except:
                    pass
        return self.attack_group, self.defend_group


    def block_battle_simulation_not_equal_unmatch(self, attack_unmatch, defend_unmatch):
        rest_attack_damage = 0
        rest_attack_health = 0
        rest_defend_damage = 0
        rest_defend_health = 0

        for block in attack_unmatch:
            rest_attack_damage += self.attack_group[block]["temp_attack_damage"]
            rest_attack_health += self.attack_group[block]["total_attack_health"]
        for block in defend_unmatch:
            rest_defend_damage += self.defend_group[block]["temp_defence_damage"]
            rest_defend_health += self.defend_group[block]["total_defence_health"]

        a_d_ratio = rest_attack_damage / rest_defend_health
        d_a_ratio = rest_defend_damage / rest_attack_health

        if a_d_ratio > d_a_ratio:
            for block in defend_unmatch:
                if self.defend_group[block].get("hero"):
                    user_hero = self.defend_group[block]["hero"]
                    user_hero.is_dead = True
                    user_hero.current_health = 0
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                    self.attacker_statistic.hero_kill += 1
                    self.defender_statistic.hero_dead += 1
                    # self.defender_deads[block]["deads"] += 1
                    if self.defend_group[block].get("hero_troop"):
                        self.attacker_statistic.kill += self.defend_group[block]["hero_troop_count"]
                        self.defender_statistic.dead += self.defend_group[block]["hero_troop_count"]
                        self.defender_deads[block]["hero_troop_deads"] += self.defend_group[block]["hero_troop_count"]
                if self.defend_group[block].get("troop"):
                    self.defender_deads[block]["user_troop"] = self.defend_group[block]["troop"]
                    self.defender_deads[block]["deads"] += self.defend_group[block]["count"]
                    self.attacker_statistic.kill += self.defend_group[block]["count"]
                    self.defender_statistic.dead += self.defend_group[block]["count"]
                self.defend_group.pop(block)
            attacker_got_damage = rest_defend_damage / a_d_ratio    
            for block in attack_unmatch:
                attacker_block_got_damage = attacker_got_damage * (self.attack_group[block]["total_attack_health"] / rest_attack_health)
                if self.attack_group[block].get("troop") and self.attack_group[block].get("hero"):
                    user_hero = self.attack_group[block]["hero"]
                    hero_summon_total_health = self.attack_group[block]["hero_troop_count"] * user_hero.hero.summon_type.health if self.attack_group[block].get("hero_troop_count") else 0
                    hero_damage_ratio = (user_hero.current_health + hero_summon_total_health) / attacker_block_got_damage
                    hero_got_damage = attacker_block_got_damage * hero_damage_ratio
                    if self.attack_group[block].get("hero_troop"):
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if (hero_got_damage / summon_health_per_troop) > self.attack_group[block]["hero_troop_count"]:
                            hero_damage_left = hero_got_damage - (summon_health_per_troop * self.attack_group[block]["hero_troop_count"])
                            self.attacker_statistic.dead += self.attack_group[block]["hero_troop_count"]
                            self.defender_statistic.kill += self.attack_group[block]["hero_troop_count"]
                            self.attacker_deads[block]["hero_troop_deads"] += self.attack_group[block]["hero_troop_count"]
                            self.attack_group[block]["hero_troop_count"] = 0
                            user_hero.current_health -= round(hero_damage_left)
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.attacker_statistic.dead += lost_troops
                            self.defender_statistic.kill += lost_troops
                            self.attacker_deads[block]["hero_troop_deads"] += lost_troops
                            self.attack_group[block]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    attacker_troop_got_damage = (1-hero_damage_ratio) * attacker_block_got_damage
                    lost_troops = math.floor((attacker_troop_got_damage / rest_attack_health) * self.attack_group[block]["count"])
                    self.attacker_deads[block]["user_troop"] = self.attack_group[block]["troop"]
                    self.attacker_deads[block]["deads"] += lost_troops
                    self.attacker_statistic.dead += lost_troops
                    self.defender_statistic.kill += lost_troops
                    self.attack_group[block]["count"] -= lost_troops
                    self.attack_group[block]["total_attack_damage"] -= self.attack_group[block]["total_attack_damage"] * attacker_block_got_damage / self.attack_group[block]["total_attack_health"]
                    self.attack_group[block]["total_attack_health"] -= attacker_block_got_damage
                elif self.attack_group[block].get("hero"):
                    user_hero = self.attack_group[block]["hero"]
                    if self.attack_group[block].get("hero_troop"):
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if (attacker_block_got_damage / summon_health_per_troop) > self.attack_group[block]["hero_troop_count"]:
                            hero_damage_left = attacker_block_got_damage - (summon_health_per_troop * self.attack_group[block]["hero_troop_count"])
                            self.attacker_statistic.dead += self.attack_group[block]["hero_troop_count"]
                            self.defender_statistic.kill += self.attack_group[block]["hero_troop_count"]
                            self.attacker_deads[block]["hero_troop_deads"] += self.attack_group[block]["hero_troop_count"]
                            self.attack_group[block]["hero_troop_count"] = 0
                            user_hero.current_health -= round(hero_damage_left)
                            user_hero.save()
                        else:
                            lost_troops = math.floor(attacker_block_got_damage / summon_health_per_troop)
                            self.attacker_statistic.dead += lost_troops
                            self.defender_statistic.kill += lost_troops
                            self.attacker_deads[block]["hero_troop_deads"] += lost_troops
                            self.attack_group[block]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(attacker_got_damage)
                        user_hero.save()
                    self.attack_group[block]["total_attack_damage"] -= self.attack_group[block]["total_attack_damage"] * attacker_block_got_damage / self.attack_group[block]["total_attack_health"]
                    self.attack_group[block]["total_attack_health"] -= attacker_block_got_damage
                elif self.attack_group[block].get("troop"):
                    lost_troops = math.floor((attacker_block_got_damage / rest_attack_health) * self.attack_group[block]["count"])
                    self.attacker_deads[block]["user_troop"] = self.attack_group[block]["troop"]
                    self.attacker_deads[block]["deads"] += lost_troops
                    self.attack_group[block]["count"] -= lost_troops
                    self.attack_group[block]["total_attack_damage"] -= self.attack_group[block]["total_attack_damage"] * attacker_block_got_damage / self.attack_group[block]["total_attack_health"]
                    self.attack_group[block]["total_attack_health"] -= attacker_block_got_damage
                    self.attacker_statistic.dead += lost_troops
                    self.defender_statistic.kill += lost_troops
                else:
                    pass
        else:
            for block in attack_unmatch:
                if self.attack_group[block].get("hero"):
                    user_hero = self.attack_group[block]["hero"]
                    user_hero.is_dead = True
                    user_hero.current_health = 0
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                    self.attacker_statistic.hero_dead += 1
                    self.defender_statistic.hero_kill += 1
                    # self.attacker_deads[block]["deads"] += 1
                if self.attack_group[block].get("hero_troop"):
                    self.attacker_statistic.dead += self.attack_group[block]["hero_troop_count"]
                    self.defender_statistic.kill += self.attack_group[block]["hero_troop_count"]
                    self.attacker_deads[block]["hero_troop_deads"] += self.attack_group[block]["hero_troop_count"]
                if self.attack_group[block].get("troop"):
                    self.attacker_statistic.dead += self.attack_group[block]["count"]
                    self.defender_statistic.kill += self.attack_group[block]["count"]
                    self.attacker_deads[block]["user_troop"] = self.attack_group[block]["troop"]
                    self.attacker_deads[block]["deads"] += self.attack_group[block]["count"]
                self.attack_group.pop(block)
            defender_got_damage = rest_attack_damage / d_a_ratio
            for block in defend_unmatch:
                defender_block_got_damage = defender_got_damage * (self.defend_group[block]["total_defence_health"] / rest_defend_health)
                if self.defend_group[block].get("hero") and self.defend_group[block].get("troop"):
                    user_hero = self.defend_group[block]["hero"]
                    hero_summon_total_health = self.defend_group[block]["hero_troop_count"] * user_hero.hero.summon_type.health if self.defend_group[block].get("hero_troop_count") else 0
                    hero_damage_ratio = (user_hero.current_health + hero_summon_total_health) / defender_block_got_damage
                    hero_got_damage = defender_block_got_damage * hero_damage_ratio
                    if self.defend_group[block].get("hero_troop"):
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if (hero_got_damage / summon_health_per_troop) > self.attack_group[block]["hero_troop_count"]:
                            hero_damage_left = hero_got_damage - (summon_health_per_troop * self.attack_group[block]["hero_troop_count"])
                            self.attacker_statistic.kill += self.defend_group[block]["hero_troop_count"]
                            self.defender_statistic.dead += self.defend_group[block]["hero_troop_count"]
                            self.defender_deads[block]["hero_troop_deads"] += self.defend_group[block]["hero_troop_count"]
                            self.defend_group[block]["hero_troop_count"] = 0
                            user_hero.current_health -= round(hero_damage_left)
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.attacker_statistic.kill += lost_troops
                            self.defender_statistic.dead += lost_troops
                            self.defender_deads[block]["hero_troop_deads"] += lost_troops
                            self.defend_group[block]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    defender_troop_got_damage = (1-hero_damage_ratio) * defender_block_got_damage    
                    lost_troops = math.floor(defender_troop_got_damage / rest_defend_health * self.defend_group[block]["count"])
                    self.defender_deads[block]["user_troop"] = self.defend_group[block]["troop"]
                    self.defender_deads[block]["deads"] += lost_troops
                    self.defend_group[block]["count"] -= lost_troops
                    self.defend_group[block]["total_defence_damage"] -= self.defend_group[block]["total_defence_damage"] * defender_block_got_damage / self.defend_group[block]["total_defence_health"]
                    self.defend_group[block]["total_defence_health"] -= defender_block_got_damage
                    self.attacker_statistic.kill += lost_troops
                    self.defender_statistic.dead += lost_troops
                elif self.defend_group[block].get("hero"):
                    user_hero = self.defend_group[block]["hero"]
                    hero_got_damage = defender_block_got_damage
                    if self.defend_group[block].get("hero_troop"):
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if (hero_got_damage / summon_health_per_troop) > self.defend_group[block]["hero_troop_count"]:
                            hero_damage_left = hero_got_damage - (summon_health_per_troop * self.defend_group[block]["hero_troop_count"])
                            self.attacker_statistic.kill += self.defend_group[block]["hero_troop_count"]
                            self.defender_statistic.dead += self.defend_group[block]["hero_troop_count"]
                            self.defender_deads[block]["hero_troop_deads"] += self.defend_group[block]["hero_troop_count"]
                            self.defend_group[block]["hero_troop_count"] = 0
                            user_hero.current_health -= round(hero_damage_left)
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.attacker_statistic.kill += lost_troops
                            self.defender_statistic.dead += lost_troops
                            self.defender_deads[block]["hero_troop_deads"] += lost_troops
                            self.defend_group[block]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    self.defend_group[block]["total_defence_damage"] -= self.defend_group[block]["total_defence_damage"] * defender_block_got_damage / self.defend_group[block]["total_defence_health"]
                    self.defend_group[block]["total_defence_health"] -= defender_block_got_damage
                elif self.defend_group[block].get("troop"):
                    defender_troop_got_damage = defender_block_got_damage    
                    lost_troops = math.floor(defender_troop_got_damage / rest_defend_health * self.defend_group[block]["count"])
                    self.defender_deads[block]["user_troop"] = self.defend_group[block]["troop"]
                    self.defender_deads[block]["deads"] += lost_troops
                    self.defend_group[block]["count"] -= lost_troops
                    self.defend_group[block]["total_defence_damage"] -= self.defend_group[block]["total_defence_damage"] * defender_block_got_damage / self.defend_group[block]["total_defence_health"]
                    self.defend_group[block]["total_defence_health"] -= defender_block_got_damage
                    self.attacker_statistic.kill += lost_troops
                    self.defender_statistic.dead += lost_troops
                else:
                    pass
        self.attacker_statistic.save()
        self.defender_statistic.save()
        return self.attack_group, self.defend_group, self.attacker_deads, self.defender_deads


    def block_battle_simulation_match(self, att_match, def_match):
        for aum, dum in zip(att_match, def_match):
            a_d_ratio = self.attack_group[aum]["temp_attack_damage"] / self.defend_group[dum]["total_defence_health"]
            d_a_ratio = self.defend_group[dum]["temp_defence_damage"] / self.attack_group[aum]["total_attack_health"]
            # IF ATTACKER WINS
            if a_d_ratio > d_a_ratio:
                # Defender's troops die
                if self.defend_group[dum].get("troop"):
                    self.defender_deads[dum]["user_troop"] = self.defend_group[dum]["troop"]
                    self.defender_deads[dum]["deads"] += self.defend_group[dum]["count"]
                    self.attacker_statistic.kill += self.defend_group[dum]["count"]
                    self.defender_statistic.dead += self.defend_group[dum]["count"]
                if self.defend_group[dum].get("hero"):
                    user_hero = self.defend_group[dum]["hero"]
                    if user_hero.hero.summon_amount != 0:
                        self.defender_deads[dum]["hero_troop_deads"] += self.defend_group[dum]["hero_troop_count"]
                        # self.defender_deads[dum]["deads"] += 1
                        self.attacker_statistic.kill += self.defend_group[dum]["hero_troop_count"]
                        self.defender_statistic.dead += self.defend_group[dum]["hero_troop_count"]
                    user_hero.is_dead = True
                    user_hero.current_health = 0
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                    self.attacker_statistic.hero_kill += 1
                    self.defender_statistic.hero_dead += 1              
                attacker_got_damage = self.defend_group[dum]["temp_defence_damage"] / a_d_ratio
                self.defend_group.pop(dum)
                # Attacker's troops die
                if self.attack_group[aum].get("hero") and self.attack_group[aum].get("troop"):
                    user_hero = self.attack_group[aum]["hero"]
                    hero_summon_total_health = self.attack_group[aum]["hero_troop_count"] * user_hero.hero.summon_type.health if self.attack_group[aum].get("hero_troop_count") else 0
                    hero_damage_ratio = (user_hero.current_health + hero_summon_total_health) / self.attack_group[aum]["total_attack_health"]
                    hero_got_damage = hero_damage_ratio * attacker_got_damage
                    if user_hero.hero.summon_amount != 0:
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if math.floor(hero_got_damage / summon_health_per_troop) > self.attack_group[aum]["hero_troop_count"]:
                            self.attacker_statistic.dead += self.attack_group[aum]["hero_troop_count"]
                            self.defender_statistic.kill += self.attack_group[aum]["hero_troop_count"]
                            self.attacker_deads[aum]["hero_troop_deads"] += self.attack_group[aum]["hero_troop_count"]
                            user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * self.attack_group[aum]["hero_troop_count"]))
                            self.attack_group[aum]["hero_troop_count"] = 0
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.attacker_statistic.dead += lost_troops
                            self.defender_statistic.kill += lost_troops
                            self.attacker_deads[aum]["hero_troop_deads"] += lost_troops
                            self.attack_group[aum]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    attacker_troop_got_damage = (1-hero_damage_ratio) * attacker_got_damage
                    lost_troops = math.floor(attacker_troop_got_damage / self.attack_group[aum]["health_per_troop"])
                    self.attacker_statistic.dead += lost_troops
                    self.defender_statistic.kill += lost_troops
                    self.attacker_deads[aum]["user_troop"] = self.attack_group[aum]["troop"]
                    self.attacker_deads[aum]["deads"] += lost_troops
                    self.attack_group[aum]["count"] -= lost_troops
                    self.attack_group[aum]["total_attack_damage"] -= self.attack_group[aum]["total_attack_damage"] * attacker_got_damage / self.attack_group[aum]["total_attack_health"]
                    self.attack_group[aum]["total_attack_health"] -= attacker_got_damage
                elif self.attack_group[aum].get("hero"):
                    user_hero = self.attack_group[aum]["hero"]
                    hero_got_damage = attacker_got_damage
                    if user_hero.hero.summon_amount != 0:
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if math.floor(hero_got_damage / summon_health_per_troop) > self.attack_group[aum]["hero_troop_count"]:
                            self.attacker_statistic.dead += self.attack_group[aum]["hero_troop_count"]
                            self.defender_statistic.kill += self.attack_group[aum]["hero_troop_count"]
                            self.attacker_deads[aum]["hero_troop_deads"] += self.attack_group[aum]["hero_troop_count"]
                            user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * self.attack_group[aum]["hero_troop_count"]))
                            self.attack_group[aum]["hero_troop_count"] = 0
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.attacker_statistic.dead += lost_troops
                            self.defender_statistic.kill += lost_troops
                            self.attacker_deads[aum]["hero_troop_deads"] += lost_troops
                            self.attack_group[aum]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    self.attack_group[aum]["total_attack_damage"] -= self.attack_group[aum]["total_attack_damage"] *  attacker_got_damage / self.attack_group[aum]["total_attack_health"]
                    self.attack_group[aum]["total_attack_health"] -= attacker_got_damage
                elif self.attack_group[aum].get("troop"):
                    lost_troops = math.floor(attacker_got_damage / self.attack_group[aum]["health_per_troop"])
                    self.attacker_statistic.dead += lost_troops
                    self.defender_statistic.kill += lost_troops
                    self.attacker_deads[aum]["user_troop"] = self.attack_group[aum]["troop"]
                    self.attacker_deads[aum]["deads"] += lost_troops
                    self.attack_group[aum]["count"] -= lost_troops
                    self.attack_group[aum]["total_attack_damage"] -= self.attack_group[aum]["total_attack_damage"] * attacker_got_damage / self.attack_group[aum]["total_attack_health"]
                    self.attack_group[aum]["total_attack_health"] -= attacker_got_damage
                else:
                    pass
            # ELSE DEFENDER WINS
            else:
                # Attacker's troops die
                if self.attack_group[aum].get("troop"):
                    self.attacker_deads[aum]["user_troop"] = self.attack_group[aum]["troop"]
                    self.attacker_deads[aum]["deads"] += self.attack_group[aum]["count"]
                    self.attacker_statistic.dead += self.attack_group[aum]["count"]
                    self.defender_statistic.kill += self.attack_group[aum]["count"]
                if self.attack_group[aum].get("hero"):
                    user_hero = self.attack_group[aum]["hero"]
                    user_hero.is_dead = True
                    user_hero.current_health = 0
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                    self.attacker_statistic.hero_dead += 1
                    self.defender_statistic.hero_kill += 1
                    # self.attacker_deads[aum]["deads"] += 1
                if self.attack_group[aum].get("hero_troop"):
                    self.attacker_statistic.dead += self.attack_group[aum]["hero_troop_count"]
                    self.defender_statistic.kill += self.attack_group[aum]["hero_troop_count"]
                    self.attacker_deads[aum]["hero_troop_deads"] += self.attack_group[aum]["hero_troop_count"]
                defender_got_damage = self.attack_group[aum]["temp_attack_damage"] / d_a_ratio
                self.attack_group.pop(aum)
                # Defender troop die
                if self.defend_group[dum].get("hero") and self.defend_group[dum].get("troop"):
                    user_hero = self.defend_group[dum]["hero"]
                    hero_summon_total_health = self.defend_group[dum]["hero_troop_count"] * user_hero.hero.summon_type.health if self.defend_group[dum].get("hero_troop_count") else 0
                    hero_damage_ratio = (user_hero.current_health + hero_summon_total_health) / self.defend_group[dum]["total_defence_health"]
                    hero_got_damage = hero_damage_ratio * defender_got_damage
                    if user_hero.hero.summon_amount != 0:
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if math.floor(hero_got_damage / summon_health_per_troop) > self.defend_group[dum]["hero_troop_count"]:
                            self.defender_statistic.dead += self.defend_group[dum]["hero_troop_count"]
                            self.attacker_statistic.kill += self.defend_group[dum]["hero_troop_count"]
                            self.defender_deads[dum]["hero_troop_deads"] += self.defend_group[dum]["hero_troop_count"]
                            user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * self.defend_group[dum]["hero_troop_count"]))
                            self.defend_group[dum]["hero_troop_count"] = 0
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.defender_statistic.dead += lost_troops
                            self.attacker_statistic.kill += lost_troops
                            self.defender_deads[dum]["hero_troop_deads"] += lost_troops
                            self.defend_group[dum]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    defender_troop_got_damage = (1-hero_damage_ratio) * defender_got_damage
                    lost_troops = math.floor(defender_troop_got_damage / ( self.defend_group[dum]["health_per_troop"]))
                    self.defender_statistic.dead += lost_troops
                    self.attacker_statistic.kill += lost_troops
                    self.defender_deads[dum]["user_troop"] = self.defend_group[dum]["troop"]
                    self.defender_deads[dum]["deads"] += lost_troops
                    self.defend_group[dum]["count"] -= lost_troops
                    self.defend_group[dum]["total_defence_damage"] -= self.defend_group[dum]["total_defence_damage"] * defender_got_damage / self.defend_group[dum]["total_defence_health"]
                    self.defend_group[dum]["total_defence_health"] -= defender_got_damage
                elif self.defend_group[dum].get("hero"):
                    user_hero = self.defend_group[dum]["hero"]
                    hero_got_damage = defender_got_damage
                    if user_hero.hero.summon_amount != 0:
                        summon_health_per_troop = user_hero.hero.summon_type.health
                        if math.floor(hero_got_damage / summon_health_per_troop) > self.defend_group[dum]["hero_troop_count"]:
                            self.defender_statistic.dead += self.defend_group[dum]["hero_troop_count"]
                            self.attacker_statistic.kill += self.defend_group[dum]["hero_troop_count"]
                            self.defender_deads[dum]["hero_troop_deads"] += self.defend_group[dum]["hero_troop_count"]
                            user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * self.defend_group[dum]["hero_troop_count"]))
                            self.defend_group[dum]["hero_troop_count"] = 0
                            user_hero.save()
                        else:
                            lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                            self.defender_statistic.dead += lost_troops
                            self.attacker_statistic.kill += lost_troops
                            self.defender_deads[dum]["hero_troop_deads"] += lost_troops
                            self.defend_group[dum]["hero_troop_count"] -= lost_troops
                    else:
                        user_hero.current_health -= round(hero_got_damage)
                        user_hero.save()
                    self.defend_group[dum]["total_defence_damage"] -= self.defend_group[dum]["total_defence_damage"] * defender_got_damage / self.defend_group[dum]["total_defence_health"]
                    self.defend_group[dum]["total_defence_health"] -= defender_got_damage
                elif self.defend_group[dum].get("troop"):
                    lost_troops = math.floor(defender_got_damage / self.defend_group[dum]["health_per_troop"])
                    self.defender_statistic.dead += lost_troops
                    self.attacker_statistic.kill += lost_troops
                    self.defender_deads[dum]["user_troop"] = self.defend_group[dum]["troop"]
                    self.defender_deads[dum]["deads"] += lost_troops
                    self.defend_group[dum]["count"] -= lost_troops
                    self.defend_group[dum]["total_defence_damage"] -= self.defend_group[dum]["total_defence_damage"] * defender_got_damage / self.defend_group[dum]["total_defence_health"]
                    self.defend_group[dum]["total_defence_health"] -= defender_got_damage
                else:
                    pass
        self.attacker_statistic.save()
        self.defender_statistic.save()
        return self.attack_group, self.defend_group, self.attacker_deads, self.defender_deads


    def arriving_create_and_resource_pillage(self):
        if not self.attack_group:
            return None
        else:
            defender_resources = Resources.objects.get(user=self.defender_user)
            # Calculate the total burden of the group
            total_burden = sum([self.attack_group[block]["troop"].troop.burden * self.attack_group[block]["count"] for block in self.blocks if self.attack_group.get(block) and self.attack_group[block].get("troop")])

            # Create arrving campaign object ---later will update after create the troops
            arriving_campaign_obj = ArrivingCampaigns.objects.create(user = self.departing_campaign.user, main_location=self.departing_campaign.target_location, target_location=self.departing_campaign.main_location, campaign_type="return")

            # WOOD
            if defender_resources.wood > total_burden / 4:
                arriving_campaign_obj.arriving_wood = math.floor(total_burden / 4)
                defender_resources.wood -= math.floor(total_burden / 4)
            else:
                arriving_campaign_obj.arriving_wood = defender_resources.wood
                defender_resources.wood = 0
            # STONE
            if defender_resources.stone > total_burden / 4:
                arriving_campaign_obj.arriving_stone = math.floor(total_burden / 4)
                defender_resources.stone -= math.floor(total_burden / 4)
            else:
                arriving_campaign_obj.arriving_stone = defender_resources.stone
                defender_resources.stone = 0
            # IRON    
            if defender_resources.iron > total_burden / 4:
                arriving_campaign_obj.arriving_iron = math.floor(total_burden /4)
                defender_resources.iron -= math.floor(total_burden / 4)
            else:
                arriving_campaign_obj.arriving_iron = defender_resources.iron
                defender_resources.iron = 0
            # GRAIN
            if defender_resources.grain > total_burden / 4:
                arriving_campaign_obj.arriving_grain = math.floor(total_burden / 4)
                defender_resources.grain -= math.floor(total_burden / 4)
            else:
                arriving_campaign_obj.arriving_grain = defender_resources.grain
                defender_resources.grain = 0
            
            if not self.defend_group:
                if defender_resources.rings != 0:
                    arriving_campaign_obj.arriving_rings = defender_resources.rings
                    defender_resources.rings = 0
                if defender_resources.the_one_ring:
                    attacker_resources = Resources.objects.get(user = self.attacker_user)
                    attacker_resources.the_one_ring = True
                    attacker_resources.save()
                    defender_resources.the_one_ring = False
                    defender_resources.save()
                    main_loc = self.departing_campaign.main_location
                    main_loc.has_ring = True
                    main_loc.save()
                    target_loc = self.departing_campaign.target_location
                    target_loc.has_ring = False
                    target_loc.save()

            arriving_campaign_obj.save()
            defender_resources.save()

            for block in self.blocks:
                if self.attack_group.get(block):
                    ArrivingTroops.objects.create(
                        user = self.departing_campaign.user,
                        user_troop = self.attack_group[block]["troop"] if self.attack_group[block].get("troop") else None,
                        count = self.attack_group[block]["count"] if self.attack_group[block].get("count") else 0,
                        campaign = arriving_campaign_obj
                    )
                    if self.attack_group[block].get("hero"):
                        ArrivingHeroes.objects.create(
                            user = self.departing_campaign.user,
                            user_hero = self.attack_group[block]["hero"],
                            campaign = arriving_campaign_obj
                        )


                    
                else:
                    ArrivingTroops.objects.create(
                        user = self.departing_campaign.user,
                        user_troop = None,
                        count = 0,
                        campaign = arriving_campaign_obj
                    )
            
            arriving_campaign_obj.time_left = round(arriving_campaign_obj.distance / arriving_campaign_obj.speed * 3600)
            arriving_campaign_obj.arriving_time = timezone.now() + timedelta(seconds=arriving_campaign_obj.time_left)
            arriving_campaign_obj.save()
            from .tasks import arriving_task
            arriving_task.apply_async(args=[arriving_campaign_obj.id], countdown=arriving_campaign_obj.time_left)
            return arriving_campaign_obj


    def delete_departing_campaign(self):
        DepartingTroops.objects.filter(campaign=self.departing_campaign).delete()
        self.departing_campaign.delete()

    
    def create_battle_report_objects(self, arriving_campaign_object):
        if not self.attack_group:
            hidden = True
        hidden = True if not self.attack_group else False
        battle = Battles.objects.create(attacker=self.attacker_user, defender=self.defender_user, battle_type=self.departing_campaign.campaign_type, is_hidden = hidden)
        for block in self.blocks:
            if self.main_attack_group.get(block):
                AttackerDeads.objects.create(
                    battle=battle,
                    user_troop = self.main_attack_group[block]["troop"] if self.main_attack_group[block].get("troop") else None,
                    troop_count = self.main_attack_group[block]["count"],
                    deads = self.attacker_deads[block]["deads"],
                    position = block,
                    status = self.attacker_deads[block]["status"],
                    user_hero = self.main_attack_group[block]["hero"] if self.main_attack_group[block].get("hero") else None,
                    user_hero_troop = self.main_attack_group[block]["hero_troop"] if self.main_attack_group[block].get("hero_troop") else None,
                    user_hero_troop_count = self.main_attack_group[block]["hero_troop_count"] if self.main_attack_group[block].get("hero_troop_count") else 0,
                    user_hero_troop_dead = self.attacker_deads[block]["hero_troop_deads"]
                )
            if self.main_defend_group.get(block):
                DefenderDeads.objects.create(
                    battle=battle,
                    user_troop = self.main_defend_group[block]["troop"] if self.main_defend_group[block].get("troop") else None,
                    troop_count = self.main_defend_group[block]["count"],
                    deads = self.defender_deads[block]["deads"],
                    position = block,
                    status = self.defender_deads[block]["status"],
                    user_hero = self.main_defend_group[block]["hero"] if self.main_defend_group[block].get("hero") else None,
                    user_hero_troop = self.main_defend_group[block]["hero_troop"] if self.main_defend_group[block].get("hero_troop") else None,
                    user_hero_troop_count = self.main_defend_group[block]["hero_troop_count"] if self.main_defend_group[block].get("hero_troop_count") else 0,
                    user_hero_troop_dead = self.defender_deads[block]["hero_troop_deads"]
                )
            
        # Defender buildings down
        if (self.departing_campaign.campaign_type == "attackblock" or self.departing_campaign.campaign_type == "attackflank") and self.attack_group:
            demolished_buildings = self.demolish_building()
            if demolished_buildings:
                for object in demolished_buildings:
                    DefenderBuildingDemolish.objects.create(
                        battle = battle,
                        building = object[0],
                        pre_battle_level = object[1],
                        post_battle_level = object[2]
                    )
        if arriving_campaign_object:
            BattlePillageResources.objects.create(
                battle = battle,
                wood = arriving_campaign_object.arriving_wood,
                stone = arriving_campaign_object.arriving_stone,
                iron = arriving_campaign_object.arriving_iron,
                grain = arriving_campaign_object.arriving_grain,
                rings = arriving_campaign_object.arriving_rings,
            )
        else:
            BattlePillageResources.objects.create(
                battle = battle
            )
                

    def delete_defender_dead_troops(self):
        defender_reinforcements = ReinforcementTroops.objects.filter(location= self.departing_campaign.target_location)
        final_deads = dict()
        # Get the user troops' and total deads number for DB update
        for key, value in self.defender_deads.items():
            if value.get("user_troop") == "":
                pass
            elif value.get("user_troop") in final_deads.keys():
                final_deads[value["user_troop"]] += value["deads"]
            else:
                final_deads.update({value["user_troop"]: value["deads"]})

        for troop, deads in final_deads.items():
            # check if the user troop is reinforcement or native
            if defender_reinforcements.filter(user_troop=troop).exists():
                rein_troop = defender_reinforcements.get(user_troop= troop)
                rein_troop.count -= deads if deads <= rein_troop.count else rein_troop.count
                rein_troop.save()
            else:
                troop.count -= deads if deads <= troop.count else troop.count
                troop.save()

        # Rest troop divider is a value that define how many percent of the troops (not in defence position) will be alive after battle. if pillage 3/4 lives, else 1/3 lives
        rest_troop_divider = 1.333 if self.departing_campaign.campaign_type == "pillage" else 3
        # IF defender loose all defence, also lost the 2/3 of the rest troops
        if not self.defend_group:
            defender_user_troops = UserTroops.objects.filter(user= self.defender_user).exclude(count=0)
            for troop in defender_user_troops:
                troop.count = math.floor(troop.count / rest_troop_divider) if troop.count > 5 else 0
                troop.save()
            # IF defender loose all defence, also lost the 2/3 of the reinforcements
            if defender_reinforcements:
                for troop in defender_reinforcements:
                    troop.count = math.floor(troop.count / rest_troop_divider) if troop.count > 5 else 0
                    troop.save()


    def block_battle_fight(self):
        war_end = False
        while not war_end:
            # MATCHES AND UNMATCHES FOR BLOCK BATTLE
            war_end, att_match, def_match, att_unmatch, def_unmatch = self.block_battle_matcher()
            if war_end:
                break
            # AFTER MATCHES, RE-CALCULETE THE DAMAGES
            self.attack_group, self.defend_group = self.block_calculations(att_match, def_match, att_unmatch, def_unmatch)
            if att_unmatch and def_unmatch:
                self.attack_group, self.defend_group, self.attacker_deads, self.defender_deads = self.block_battle_simulation_not_equal_unmatch(att_unmatch, def_unmatch)
            # Defender has extra troop/block
            elif not att_unmatch and def_unmatch:
                rest_temp_damage = 0
                for block in def_unmatch:
                    rest_temp_damage += self.defend_group[block]["temp_defence_damage"]
                for block in def_match:
                    self.defend_group[block]["temp_defence_damage"] += rest_temp_damage / len(def_match)
            # Attacker has extra troop/block
            elif att_unmatch and not def_unmatch:
                rest_temp_damage = 0
                for block in att_unmatch:
                    rest_temp_damage += self.attack_group[block]["temp_attack_damage"]
                for block in att_match:
                    self.attack_group[block]["temp_attack_damage"] += rest_temp_damage / len(att_match)
            else:
                pass

            # MATCHES BATTLE
            if att_match:
                self.attack_group, self.defend_group, self.attacker_deads, self.defender_deads = self.block_battle_simulation_match(att_match, def_match)
                
            # Deads status update
        for block in self.blocks:
            try:
                if self.defender_deads[block]["deads"] == self.main_defend_group[block]["count"]:
                    self.defender_deads[block].update({"status": "dead"})
                elif self.defender_deads[block]["deads"] != 0:
                    self.defender_deads[block].update({"status": "injured"})
                else:
                    self.defender_deads[block].update({"status": "ok"})
            except:
                self.defender_deads[block].update({"status": "dead"})

            try:
                if self.attacker_deads[block]["deads"] == self.main_attack_group[block]["count"]:
                    self.attacker_deads[block].update({"status": "dead"})
                elif self.attacker_deads[block]["deads"] != 0:
                    self.attacker_deads[block].update({"status": "injured"})
                else:
                    self.attacker_deads[block].update({"status": "ok"})
            except:
                self.attacker_deads[block].update({"status": "dead"})


        return self.attack_group, self.defend_group, self.main_attack_group, self.main_defend_group, self.attacker_deads, self.defender_deads


    def flank_battle_matcher(self):
        war_end = False
        # IF one the group has extinct, war is ended TRUE
        if not self.attack_group.keys() or not self.defend_group.keys():
            war_end = True
            att_match = []
            def_match = []
            att_unmatch = []
            def_unmatch = []
            return war_end, att_match, att_unmatch, def_match, def_unmatch
        else:
            att_match = []
            def_match = []
            att_unmatch = []
            def_unmatch = []
            # Create a nested list for each column
            attack_flank_positions = [
                [x for x in self.attack_group.keys() if x % 10 == 1],
                [x for x in self.attack_group.keys() if x % 10 == 2],
                [x for x in self.attack_group.keys() if x % 10 == 3],
                [x for x in self.attack_group.keys() if x % 10 == 4]
            ]

            defend_flank_positions = [
                [x for x in self.defend_group.keys() if x % 10 == 1],
                [x for x in self.defend_group.keys() if x % 10 == 2],
                [x for x in self.defend_group.keys() if x % 10 == 3],
                [x for x in self.defend_group.keys() if x % 10 == 4]
            ]

            # for 4 columns check the front blocks and match them
            for line in range(4):
                if attack_flank_positions[line] != [] and defend_flank_positions[line] != []:
                    att_match.append(attack_flank_positions[line][0])
                    def_match.append(defend_flank_positions[line][0])
                    # remove the matches from current positions
                    attack_flank_positions[line].pop(0)
                    defend_flank_positions[line].pop(0)
                # get the free attacker block
                elif attack_flank_positions[line]:
                    att_unmatch.append(attack_flank_positions[line][0])
                # get the free defender
                # elif defend_flank_positions[line]:
                #     def_unmatch.append(defend_flank_positions[line][0])
                else:
                    pass
            # get a regular list for all defender positions and sort it. Free attacker will match from the back of the defender
            defends = [x for y in defend_flank_positions for x in y]
            defends.sort()
            if att_unmatch:
                for i in att_unmatch:
                    if defends and defends[-1] not in def_match:
                        att_match.append(i)
                        att_unmatch.remove(i)
                        def_match.append(defends[-1])
                        defends.remove(defends[-1])
                        

            matches = list(zip(att_match, def_match))
            return war_end, att_match, def_match, att_unmatch, def_unmatch


    def flank_battle_fight(self):
        war_end = False
        while not war_end:
            # MATCHES AND UNMATCHES FOR BLOCK BATTLE
            war_end, att_match, def_match, att_unmatch, def_unmatch = self.flank_battle_matcher()
            if war_end:
                break
            # AFTER MATCHES, RE-CALCULETE THE DAMAGES
            self.attack_group, self.defend_group = self.block_calculations(att_match, def_match, att_unmatch, def_unmatch)
            if att_unmatch and def_unmatch:
                self.attack_group, self.defend_group, self.attacker_deads, self.defender_deads = self.block_battle_simulation_not_equal_unmatch(att_unmatch, def_unmatch)
            # Defender has extra troop/block
            elif not att_unmatch and def_unmatch:
                rest_temp_damage = 0
                for block in def_unmatch:
                    rest_temp_damage += self.defend_group[block]["temp_defence_damage"]
                for block in def_match:
                    self.defend_group[block]["temp_defence_damage"] += rest_temp_damage / len(def_match)
            # Attacker has extra troop/block
            elif att_unmatch and not def_unmatch:
                rest_temp_damage = 0
                for block in att_unmatch:
                    rest_temp_damage += self.attack_group[block]["temp_attack_damage"]
                for block in att_match:
                    self.attack_group[block]["temp_attack_damage"] += rest_temp_damage / len(att_match)
            else:
                pass

            # MATCHES BATTLE
            if att_match:
                self.attack_group, self.defend_group, self.attacker_deads, self.defender_deads = self.block_battle_simulation_match(att_match, def_match)
                
            # Deads status update
        for block in self.blocks:
            try:
                if self.defender_deads[block]["deads"] == self.main_defend_group[block]["count"]:
                    self.defender_deads[block].update({"status": "dead"})
                elif self.defender_deads[block]["deads"] != 0:
                    self.defender_deads[block].update({"status": "injured"})
                else:
                    self.defender_deads[block].update({"status": "ok"})
            except:
                self.defender_deads[block].update({"status": "dead"})

            try:
                if self.attacker_deads[block]["deads"] == self.main_attack_group[block]["count"]:
                    self.attacker_deads[block].update({"status": "dead"})
                elif self.attacker_deads[block]["deads"] != 0:
                    self.attacker_deads[block].update({"status": "injured"})
                else:
                    self.attacker_deads[block].update({"status": "ok"})
            except:
                self.attacker_deads[block].update({"status": "dead"})


        return self.attack_group, self.defend_group, self.main_attack_group, self.main_defend_group, self.attacker_deads, self.defender_deads


    def pillage_battle_calculator(self):
        defender_type_count = {
            "infantry": 0,
            "pike": 0,
            "archer": 0,
            "cavalry": 0,
            "monster": 0,
            "siege": 0,
            "builder": 0
        }
        attacker_type_count = {
            "infantry": 0,
            "pike": 0,
            "archer": 0,
            "cavalry": 0,
            "monster": 0,
            "siege": 0,
            "builder": 0
        }
        # Get the number for each type and total number
        total_attack_damage = 1
        total_attack_health = 1
        for block, value in self.attack_group.items():
            total_attack_damage += value["total_attack_damage"]
            total_attack_health += value["total_attack_health"]
            if value.get("troop"):
                attacker_type_count[value["troop"].troop.type] += value["count"]
            if value.get("hero_troop"):
                attacker_type_count[value["hero_troop"].type] += value["hero_troop_count"]
            if value.get("hero"):
                attacker_type_count[value["hero"].hero.type] += 1
        total_attack_number = sum(attacker_type_count.values())
        
        
        total_defence_damage = 1
        total_defence_health = 1
        # Add defensive buildings' damage
        total_defence_damage += self.defensive_building_damages()

        for block, value in self.defend_group.items():
            total_defence_damage += value["total_defence_damage"]
            total_defence_health += value["total_defence_health"]
            if value.get("troop"):
                defender_type_count[value["troop"].troop.type] += value["count"]
            if value.get("hero_troop"):
                defender_type_count[value["hero_troop"].type] += value["hero_troop_count"]
            if value.get("hero"):
                defender_type_count[value["hero"].hero.type] += 1
        total_defend_number = sum(defender_type_count.values())
        total_defend_number = 1 if total_defend_number < 1 else total_defend_number

        # get the ratio's for each 
        for troop_type in attacker_type_count.keys():
            attacker_type_count[troop_type] = round(attacker_type_count[troop_type] / total_attack_number, 2)
            defender_type_count[troop_type] = round(defender_type_count[troop_type] / total_defend_number, 2)
        
        final_attack_damage = 0
        final_defence_damage = 0
        
        for attack_key, attack_value in attacker_type_count.items():
            for defence_key, defence_value in defender_type_count.items():
                final_attack_damage += attack_value * total_attack_damage * defence_value * troop_type_attack_ratio(attack_key, defence_key)
                final_defence_damage += defence_value * total_defence_damage * attack_value * troop_type_attack_ratio(defence_key, attack_key)
        attacker_dead_ratio = final_defence_damage / total_attack_health if final_defence_damage / total_attack_health < 1 else 1
        defender_dead_ratio = final_attack_damage / total_defence_health if final_attack_damage / total_defence_health < 1 else 1

        return attacker_dead_ratio, defender_dead_ratio
            
        
    def pillage_battle_deads(self):
        attacker_dead_ratio, defender_dead_ratio = self.pillage_battle_calculator()
        for block in self.blocks:
            if self.attack_group.get(block):
                if self.attack_group[block].get("troop"):
                    self.attacker_deads[block]["user_troop"] = self.attack_group[block]["troop"]
                    self.attacker_deads[block]["deads"] = round(self.attack_group[block]["count"] * attacker_dead_ratio)
                    self.attack_group[block]["count"] -= self.attacker_deads[block]["deads"]
                if self.attack_group[block].get("hero"):
                    if attacker_dead_ratio >= 1:
                        self.attack_group[block]["hero"].is_dead = True
                        self.attack_group[block]["hero"].current_health = 0
                        self.attack_group[block]["hero"].last_checkout = timezone.now()
                        self.attack_group[block]["hero"].save()
                    else:
                        self.attack_group[block]["hero"].current_health -= round(self.attack_group[block]["hero"].current_health * attacker_dead_ratio)
                        self.attack_group[block]["hero"].save()
                if self.attack_group[block].get("hero_troop_count"):
                    self.attacker_deads[block]["hero_troop_deads"] = round(self.attack_group[block]["hero_troop_count"] * attacker_dead_ratio)
                    self.attack_group[block]["hero_troop_count"] =  round(self.attack_group[block]["hero_troop_count"] * (1-attacker_dead_ratio))
                if attacker_dead_ratio == 1:
                    self.attacker_deads[block].update({"status": "dead"})
                    self.attack_group.pop(block)
                else:
                    self.attacker_deads[block].update({"status": "injured"})

            if self.defend_group.get(block):
                if self.defend_group[block].get("troop"):
                    self.defender_deads[block]["user_troop"] = self.defend_group[block]["troop"]
                    self.defender_deads[block]["deads"] = round(self.defend_group[block]["count"] * defender_dead_ratio)
                    self.defend_group[block]["count"] -= self.defender_deads[block]["deads"]
                if self.defend_group[block].get("hero"):
                    if defender_dead_ratio >= 1:
                        self.defend_group[block]["hero"].is_dead = True
                        self.defend_group[block]["hero"].current_health = 0
                        self.defend_group[block]["hero"].save()
                    else:
                        self.defend_group[block]["hero"].current_health -= round(self.defend_group[block]["hero"].current_health * defender_dead_ratio)
                        self.defend_group[block]["hero"].save()
                if self.defend_group[block].get("hero_troop_count"):
                    self.defender_deads[block]["hero_troop_deads"] = round(self.defend_group[block]["hero_troop_count"] * defender_dead_ratio)
                    self.defend_group[block]["hero_troop_count"] =  round(self.defend_group[block]["hero_troop_count"] * (1-defender_dead_ratio))
                if defender_dead_ratio == 1:
                    self.defender_deads[block].update({"status": "dead"})
                else:
                    self.defender_deads[block].update({"status": "injured"})


    def pillage_battle_fight(self):
        self.pillage_battle_calculator()
        self.pillage_battle_deads()
        return self.attack_group, self.defend_group, self.main_attack_group, self.main_defend_group, self.attacker_deads, self.defender_deads

    def demolish_building(self):
        building_demolish = list()
        if not self.attack_group:
            return building_demolish
        else:
            damage = 0
            for group in self.attack_group.values():
                if group.get("troop"):
                    if group["troop"].troop.type == "siege":
                        damage += group["troop"].troop.damage * group["count"] * group["troop"].attack_level
            if damage == 0:
                return building_demolish
            else:
                defender_buildings = UserBuildings.objects.filter(user= self.defender_user).order_by('building__health')
                
                while damage > 1000 and len(defender_buildings) > 0:
                    defender_buildings = list(defender_buildings)
                    if damage > defender_buildings[0].current_health:
                        damage -= defender_buildings[0].current_health
                        building_demolish.append([defender_buildings[0].building, defender_buildings[0].level, 0])
                        defender_buildings[0].delete()
                        defender_buildings.pop(0)
                    else:
                        level_down = math.floor(damage / 1500)
                        building_demolish.append([defender_buildings[0].building, defender_buildings[0].level, defender_buildings[0].level - level_down])
                        try:
                            defender_buildings[0].level -= level_down
                        except:
                            defender_buildings[0].level = 1
                        defender_buildings[0].save()
                        damage = 0
                return building_demolish
                        


    def defensive_building_damages(self):
        defence_building_damage = 0
        user_defensive_buildings = UserBuildings.objects.filter(user=self.defender_user, building__type="defence")
        if user_defensive_buildings.exists():
            for building in user_defensive_buildings:
                defence_building_damage += building.user_building_damage
            
            return defence_building_damage
        else:
            return 0

 


# SOME FUNCTIONS

def attack_ratio(user_troop_attacker, user_troop_defender):
    ratio = {
        "infantrypike": 1.4,
        "infantryarcher": 1.2,
        "infantrycavalry": 0.8,
        "infantrymonster": 0.8,
        "archerinfantry": 0.8,
        "archerpike": 0.8,
        "archercavalry": 0.6,
        "archermonster": 1.2,
        "pikeinfantry": 0.8,
        "pikecavalry": 1.5,
        "pikemonster": 1.3,
        "cavalryinfantry": 1.2,
        "cavalrypike": 0.6,
        "cavalryarcher": 1.8,
        "monsterinfantry": 1.3,
        "monsterarcher": 1.2,
        "monsterpike": 0.7,
        "siegeinfantry": 0.2,
        "siegepike": 0.2,
        "siegearcher": 0.25,
        "siegecavalry": 0.1,
        "siegemonster": 0.15,

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

def troop_type_attack_ratio(user_troop_attacker, user_troop_defender):
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
        "monsterpike": 0.7,
        "siegeinfantry": 0.2,
        "siegepike": 0.2,
        "siegearcher": 0.25,
        "siegecavalry": 0.1,
        "siegemonster": 0.15,

    }
    compete = user_troop_attacker + user_troop_defender
    if compete in ratio.keys():
        return ratio[compete]
    else:
        return 1
