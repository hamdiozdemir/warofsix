from encampment.models import DefencePosition, DepartingCampaigns
from main.models import UserHeroes, UserBuildings, Statistic, UserTroops
from django.db.models import Q
import math





class Attacker():

    def __init__(self, attack_group, user_heroes):
        self.attack_group = attack_group
        self.user_heroes = user_heroes
    
    def get_attack_troops(self):
        positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        group = {}
        for pos in positions:
            # If there are both TROOP and HERO
            if self.attack_group.filter(position=pos).exclude(count=0).exists() and self.user_heroes.filter(position=pos).exclude(is_dead=True).exists():
                block_troop = self.attack_group.get(position=pos)
                user_troop = block_troop.user_troop
                group[pos] = {"troop": user_troop}
                hero = self.user_heroes.get(position=pos)
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
            elif self.user_heroes.filter(position=pos).exclude(is_dead=True).exists():
                hero = self.user_heroes.get(position=pos)
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
                group[pos].update({"count": 1})
            
            else:
                pass
        return group
    


class Defender():

    def __init__(self, defender_group, user_heroes, user):
        self.defender_group = defender_group
        self.user_heroes = user_heroes
        self.user = user

    def get_defend_troops(self):
        positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        group = {}
        for pos in positions:
            # IF there are both TROOP and HERO
            if self.defender_group.filter(position=pos).exclude(percent=0).exists() and self.user_heroes.filter(position=pos).exclude(is_dead=True).exists():
                block_troop = self.defender_group.get(position=pos)
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

            elif self.defender_group.filter(position=pos).exclude(percent=0).exists():
                block_troop = self.defender_group.get(position=pos)
                user_troop = block_troop.user_troop
                group[pos] = {"troop": user_troop}
                group[pos].update({"health_per_troop": user_troop.troop.health * user_troop.defence_level})
                group[pos].update({"total_defence_health": block_troop.count * user_troop.troop.health * user_troop.defence_level})
                group[pos].update({"total_defence_damage": block_troop.count * user_troop.troop.damage * user_troop.attack_level})
                group[pos].update({"count": block_troop.count})

            elif self.user_heroes.filter(position=pos).exclude(is_dead=True).exists():
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
    
    def get_defender_user(self):
        return self.user


class BlockBattle2():

    def __init__(self, attack_group, attack_user, defend_group, defend_user):
        self.attack_group = attack_group
        self.attack_user = attack_user
        self.defend_group = defend_group
        self.defend_user = defend_user


    def full_battle(self):
        # 1. AŞAMA = match olanları al
        # 2. AŞAMA = match olanların calculation işlemi
        # 3. AŞAMA = battle fonksiyonlarını çağır

        
        pass

    
    def first_block(self):
        # Defense Towers damage will include
        # Archers damage will include OR siege damage will 

        first_block = [11,12,13,14]
        second_block = [21,22,23,24]
        third_block = [31,32,33,34]

        attacker_statistic = Statistic.objects.get(user=self.attack_user)
        defender_statistic = Statistic.objects.get(user=self.defend_user)
        defender_deads = {
            11:{"user_troop":"", "deads":0},
            12:{"user_troop":"", "deads":0},
            13:{"user_troop":"", "deads":0},
            14:{"user_troop":"", "deads":0},
            21:{"user_troop":"", "deads":0},
            22:{"user_troop":"", "deads":0},
            23:{"user_troop":"", "deads":0},
            24:{"user_troop":"", "deads":0},
            31:{"user_troop":"", "deads":0},
            32:{"user_troop":"", "deads":0},
            33:{"user_troop":"", "deads":0},
            34:{"user_troop":"", "deads":0}
        }
        attacker_deads = {
            11:{"user_troop":"", "deads":0},
            12:{"user_troop":"", "deads":0},
            13:{"user_troop":"", "deads":0},
            14:{"user_troop":"", "deads":0},
            21:{"user_troop":"", "deads":0},
            22:{"user_troop":"", "deads":0},
            23:{"user_troop":"", "deads":0},
            24:{"user_troop":"", "deads":0},
            31:{"user_troop":"", "deads":0},
            32:{"user_troop":"", "deads":0},
            33:{"user_troop":"", "deads":0},
            34:{"user_troop":"", "deads":0}
        }
        
        # DEFENSIVE BULDINGS' DAMAGE
        defender_building_damage = 0
        defender_towers = UserBuildings.objects.filter(user=self.defend_user)
        for building in defender_towers:
            defender_building_damage += building.building.damage * building.level * 0.5
        
        match_number = 0
        matches = []
        attack_unmatched = []
        defend_unmatched = []

        war_end, attack_match, defend_match, attack_unmatched, defend_unmatched = block_matcher(self.attack_group, self.defend_group)
        match_number = len(attack_match)


        # MATCHES & CALCULATIONS
        for block in first_block:
            # if both side have troop in block
            if self.attack_group.get(block) and self.defend_group.get(block):
                match_number += 1
                matches.append(block)

                # Attack Stats Update
                att_ratio = attack_ratio(self.attack_group[block]["troop"], self.defend_group[block]["troop"])
                self.attack_group[block].update({"temp_attack_damage": self.attack_group[block]["total_attack_damage"] * att_ratio})
                # CHECK IF ARCHER/SIEGE BEHIND
                if self.attack_group.get(block+10) and (self.attack_group[block+10]["troop"].troop.type == "archer" or self.attack_group[block+10]["troop"].troop.type == "siege"):
                    if self.attack_group[block+10].get("hero"):
                        hero_bonus = hero_attack_bonus(self.attack_group[block+10]["hero"], self.attack_group[block+10]["troop"])
                    else:
                        hero_bonus = 1
                    att_ratio = attack_ratio(self.attack_group[block+10]["troop"], self.defend_group[block]["troop"])
                    archer_damage = self.attack_group[block+10]["count"] * self.attack_group[block+10]["troop"].attack_level * self.attack_group[block+10]["troop"].troop.damage * hero_bonus * att_ratio
                    self.attack_group[block]["temp_attack_damage"] += archer_damage


                # Defender Stats Update
                att_ratio(self.defend_group[block]["troop"], self.attack_group[block]["troop"])
                self.defend_group[block].update({"temp_defence_damage": self.defend_group[block]["total_defence_damage"] * att_ratio + (defender_building_damage / 4)})
                # CHECK IF ARCHER/SIEGE BEHIND
                if self.defend_group.get(block+10) and (self.defend_group[block+10]["troop"].troop.type == "archer"or self.defend_group[block+10]["troop"].troop.type == "siege"):
                    if self.defend_group[block+10].get("hero"):
                        hero_bonus = hero_attack_bonus(self.defend_group[block+10]["hero"], self.defend_group[block+10]["troop"])
                    else:
                        hero_bonus = 1
                    
                    att_ratio = attack_ratio(self.defend_group[block+10]["troop"], self.attack_group[block]["troop"])
                    archer_damage = self.defend_group[block+10]["count"] * self.defend_group[block+10]["troop"].attack_level * self.defend_group[block+10]["troop"].troop.damage * hero_bonus * att_ratio

                    self.defend_group[block]["temp_defence_damage"] += archer_damage

            # only attacker has troop in block
            elif self.attack_group.get(block):
                attack_unmatched.append(block)
                self.attack_group[block].update({"temp_attack_damage": self.attack_group[block]["total_attack_damage"] * att_ratio})
                # CHECK IF ARCHER/SIEGE BEHIND
                if self.attack_group.get(block+10) and (self.attack_group[block+10]["troop"].troop.type == "archer" or self.attack_group[block+10]["troop"].troop.type == "siege"):
                    if self.attack_group[block+10].get("hero"):
                        hero_bonus = hero_attack_bonus(self.attack_group[block+10]["hero"], self.attack_group[block+10]["troop"])
                    else:
                        hero_bonus = 1
                    att_ratio = attack_ratio(self.attack_group[block+10]["troop"], self.defend_group[block]["troop"])
                    archer_damage = self.attack_group[block+10]["count"] * self.attack_group[block+10]["troop"].attack_level * self.attack_group[block+10]["troop"].troop.damage * hero_bonus
                    self.attack_group[block]["temp_attack_damage"] += archer_damage
            
            # only defender has troop in block
            elif self.defend_group.get(block):
                defend_unmatched.append(block)
                self.defend_group[block].update({"temp_defence_damage": self.defend_group[block]["total_defence_damage"] + (defender_building_damage / 4)})
                # CHECK IF ARCHER/SIEGE BEHIND
                if self.defend_group.get(block+10) and (self.defend_group[block+10]["troop"].troop.type == "archer"or self.defend_group[block+10]["troop"].troop.type == "siege"):
                    if self.defend_group[block+10].get("hero"):
                        hero_bonus = hero_attack_bonus(self.defend_group[block+10]["hero"], self.defend_group[block+10]["troop"])
                    else:
                        hero_bonus = 1
                    
                    att_ratio = attack_ratio(self.defend_group[block+10]["troop"], self.attack_group[block]["troop"])
                    archer_damage = self.defend_group[block+10]["count"] * self.defend_group[block+10]["troop"].attack_level * self.defend_group[block+10]["troop"].troop.damage * hero_bonus * att_ratio

                    self.defend_group[block]["temp_defence_damage"] += archer_damage
            
            else:
                pass


        # FIRST BLOCK READY TO BATTLE
        if len(attack_unmatched) == 0 and len(defend_unmatched) == 0:
            pass

        elif len(attack_unmatched) == len(defend_unmatched):
            pass
        else:
            pass

# SOME FUNCTIONS

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




#bunu düzenle aum ve dum         
def block_battle_simulation_match(att_match, def_match, attack_group, defend_group, attacker_deads, defender_deads, attacker_statistic, defender_statistic):
    for aum, dum in zip(att_match, def_match):
        a_d_ratio = attack_group[aum]["temp_attack_damage"] / defend_group[dum]["total_defence_health"]
        d_a_ratio = defend_group[dum]["temp_defence_damage"] / attack_group[aum]["total_attack_health"]
        # IF ATTACKER WINS
        if a_d_ratio > d_a_ratio:
            # Defender's troops die
            if defend_group[dum].get("troop"):
                defender_deads[dum]["user_troop"] = defend_group[dum]["troop"]
                defender_deads[dum]["deads"] += defend_group[dum]["count"]
                attacker_statistic.kill += defend_group[dum]["count"]
                defender_statistic.dead += defend_group[dum]["count"]
            if defend_group[dum].get("hero"):
                user_hero = defend_group[dum]["hero"]
                if user_hero.hero.summon_amount != 0:
                    defender_deads[dum]["hero_troop_deads"] += defend_group[dum]["hero_troop_count"]
                    attacker_statistic.kill += defend_group[dum]["hero_troop_count"]
                    defender_statistic.dead += defend_group[dum]["hero_troop_count"]
                user_hero.is_dead = True
                user_hero.current_health = 0
                user_hero.save()
                attacker_statistic.hero_kill += 1
                defender_statistic.hero_dead += 1              
            attacker_got_damage = defend_group[dum]["temp_defence_damage"] / a_d_ratio
            defend_group.pop(dum)

            # Attacker's troops die
            if attack_group[aum].get("hero") and attack_group[aum].get("troop"):
                user_hero = attack_group[aum]["hero"]
                hero_damage_ratio = user_hero.current_health / attack_group[aum]["total_attack_health"]
                hero_got_damage = hero_damage_ratio * attacker_got_damage
                if user_hero.hero.summon_amount != 0:
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if math.floor(hero_got_damage / summon_health_per_troop) > attack_group[aum]["hero_troop_count"]:
                        attacker_statistic.dead += attack_group[aum]["hero_troop_count"]
                        defender_statistic.kill += attack_group[aum]["hero_troop_count"]
                        attacker_deads[aum]["hero_troop_deads"] += attack_group[aum]["hero_troop_count"]
                        user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * attack_group[aum]["hero_troop_count"]))
                        attack_group[aum]["hero_troop_count"] = 0
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        attacker_statistic.dead += lost_troops
                        defender_statistic.kill += lost_troops
                        attacker_deads[aum]["hero_troop_deads"] += lost_troops
                        attack_group[aum]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()
                attacker_troop_got_damage = (1-hero_damage_ratio) * attacker_got_damage
                lost_troops = math.floor(attacker_troop_got_damage / attack_group[aum]["health_per_troop"])
                attacker_statistic.dead += lost_troops
                defender_statistic.kill += lost_troops
                attacker_deads[aum]["user_troop"] = attack_group[aum]["troop"]
                attacker_deads[aum]["deads"] += lost_troops
                attack_group[aum]["count"] -= lost_troops
                attack_group[aum]["total_attack_damage"] -= attack_group[aum]["total_attack_damage"] * attacker_got_damage / attack_group[aum]["total_attack_health"]
                attack_group[aum]["total_attack_health"] -= attacker_got_damage
            elif attack_group[aum].get("hero"):
                user_hero = attack_group[aum]["hero"]
                hero_got_damage = attacker_got_damage
                if user_hero.hero.summon_amount != 0:
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if math.floor(hero_got_damage / summon_health_per_troop) > attack_group[aum]["hero_troop_count"]:
                        attacker_statistic.dead += attack_group[aum]["hero_troop_count"]
                        defender_statistic.kill += attack_group[aum]["hero_troop_count"]
                        attacker_deads[aum]["hero_troop_deads"] += attack_group[aum]["hero_troop_count"]
                        user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * attack_group[aum]["hero_troop_count"]))
                        attack_group[aum]["hero_troop_count"] = 0
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        attacker_statistic.dead += lost_troops
                        defender_statistic.kill += lost_troops
                        attacker_deads[aum]["hero_troop_deads"] += lost_troops
                        attack_group[aum]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()
                attack_group[aum]["total_attack_damage"] -= attack_group[aum]["total_attack_damage"] *  attacker_got_damage / attack_group[aum]["total_attack_health"]
                attack_group[aum]["total_attack_health"] -= attacker_got_damage
            elif attack_group[aum].get("troop"):
                lost_troops = math.floor(attacker_got_damage / attack_group[aum]["health_per_troop"])
                attacker_statistic.dead += lost_troops
                defender_statistic.kill += lost_troops
                attacker_deads[aum]["user_troop"] = attack_group[aum]["troop"]
                attacker_deads[aum]["deads"] += lost_troops
                attack_group[aum]["count"] -= lost_troops
                attack_group[aum]["total_attack_damage"] -= attack_group[aum]["total_attack_damage"] * attacker_got_damage / attack_group[aum]["total_attack_health"]
                attack_group[aum]["total_attack_health"] -= attacker_got_damage
            else:
                pass

        # ELSE DEFENDER WINS
        else:
            # Attacker's troops die
            if attack_group[aum].get("troop"):
                attacker_deads[aum]["user_troop"] = attack_group[aum]["troop"]
                attacker_deads[aum]["deads"] += attack_group[aum]["count"]
                attacker_statistic.dead += attack_group[aum]["count"]
                defender_statistic.kill += attack_group[aum]["count"]
            if attack_group[aum].get("hero"):
                user_hero = attack_group[aum]["hero"]
                user_hero.is_dead = True
                user_hero.current_health = 0
                user_hero.save()
                attacker_statistic.hero_dead += 1
                defender_statistic.hero_kill += 1
            if attack_group[aum].get("hero_troop"):
                attacker_statistic.dead += attack_group[aum]["hero_troop_count"]
                defender_statistic.kill += attack_group[aum]["hero_troop_count"]
                attacker_deads[aum]["hero_troop_deads"] += attack_group[aum]["hero_troop_count"]
            defender_got_damage = attack_group[aum]["temp_attack_damage"] / d_a_ratio
            attack_group.pop(aum)

            # Defender troop die
            if defend_group[dum].get("hero") and defend_group[dum].get("troop"):
                user_hero = defend_group[dum]["hero"]
                hero_damage_ratio = user_hero.current_health / defend_group[dum]["total_defence_health"]
                hero_got_damage = hero_damage_ratio * defender_got_damage
                if user_hero.hero.summon_amount != 0:
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if math.floor(hero_got_damage / summon_health_per_troop) > defend_group[dum]["hero_troop_count"]:
                        defender_statistic.dead += defend_group[dum]["hero_troop_count"]
                        attacker_statistic.kill += defend_group[dum]["hero_troop_count"]
                        defender_deads[dum]["hero_troop_deads"] += defend_group[dum]["hero_troop_count"]
                        user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * defend_group[dum]["hero_troop_count"]))
                        defend_group[dum]["hero_troop_count"] = 0
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        defender_statistic.dead += lost_troops
                        attacker_statistic.kill += lost_troops
                        defender_deads[dum]["hero_troop_deads"] += lost_troops
                        defend_group[dum]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()

                defender_troop_got_damage = (1-hero_damage_ratio) * defender_got_damage
                lost_troops = math.floor(defender_troop_got_damage / ( defend_group[dum]["health_per_troop"]))
                defender_statistic.dead += lost_troops
                attacker_statistic.kill += lost_troops
                defender_deads[dum]["user_troop"] = defend_group[dum]["troop"]
                defender_deads[dum]["deads"] += lost_troops
                defend_group[dum]["count"] -= lost_troops
                defend_group[dum]["total_defence_damage"] -= defend_group[dum]["total_defence_damage"] * defender_got_damage / defend_group[dum]["total_defence_health"]
                defend_group[dum]["total_defence_health"] -= defender_got_damage
            elif defend_group[dum].get("hero"):
                user_hero = defend_group[dum]["hero"]
                hero_got_damage = defender_got_damage
                if user_hero.hero.summon_amount != 0:
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if math.floor(hero_got_damage / summon_health_per_troop) > defend_group[dum]["hero_troop_count"]:
                        defender_statistic.dead += defend_group[dum]["hero_troop_count"]
                        attacker_statistic.kill += defend_group[dum]["hero_troop_count"]
                        defender_deads[dum]["hero_troop_deads"] += defend_group[dum]["hero_troop_count"]
                        user_hero.current_health -= round(hero_got_damage - (summon_health_per_troop * defend_group[dum]["hero_troop_count"]))
                        defend_group[dum]["hero_troop_count"] = 0
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        defender_statistic.dead += lost_troops
                        attacker_statistic.kill += lost_troops
                        defender_deads[dum]["hero_troop_deads"] += lost_troops
                        defend_group[dum]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()
                defend_group[dum]["total_defence_damage"] -= defend_group[dum]["total_defence_damage"] * defender_got_damage / defend_group[dum]["total_defence_health"]
                defend_group[dum]["total_defence_health"] -= defender_got_damage
            elif defend_group[dum].get("troop"):
                lost_troops = math.floor(defender_got_damage / defend_group[dum]["health_per_troop"])
                defender_statistic.dead += lost_troops
                attacker_statistic.kill += lost_troops
                defender_deads[dum]["user_troop"] = defend_group[dum]["troop"]
                defender_deads[dum]["deads"] += lost_troops
                defend_group[dum]["count"] -= lost_troops
                defend_group[dum]["total_defence_damage"] -= defend_group[dum]["total_defence_damage"] * defender_got_damage / defend_group[dum]["total_defence_health"]
                defend_group[dum]["total_defence_health"] -= defender_got_damage
            else:
                pass
    attacker_statistic.save()
    defender_statistic.save()
    return attack_group, defend_group, attacker_deads, defender_deads


def block_battle_simulation_not_equal_unmatch(attack_unmatch, defend_unmatch, attack_group, defend_group, attacker_deads, defender_deads, attacker_statistic, defender_statistic):
    rest_attack_damage = 0
    rest_attack_health = 0
    rest_defend_damage = 0
    rest_defend_health = 0

    for block in attack_unmatch:
        rest_attack_damage += attack_group[block]["temp_attack_damage"]
        rest_attack_health += attack_group[block]["total_attack_health"]
    for block in defend_unmatch:
        rest_defend_damage += defend_group[block]["temp_defence_damage"]
        rest_defend_health += defend_group[block]["total_defence_health"]

    a_d_ratio = rest_attack_damage / rest_defend_health
    d_a_ratio = rest_defend_damage / rest_attack_health

    if a_d_ratio > d_a_ratio:
        for block in defend_unmatch:
            if defend_group[block].get("hero"):
                user_hero = defend_group[block]["hero"]
                user_hero.is_dead = True
                user_hero.current_health = 0
                user_hero.save()
                attacker_statistic.hero_kill += 1
                defender_statistic.hero_dead += 1
                if defend_group[block].get("hero_troop"):
                    attacker_statistic.kill += defend_group[block]["hero_troop_count"]
                    defender_statistic.dead += defend_group[block]["hero_troop_count"]
                    defender_deads[block]["hero_troop_deads"] += defend_group[block]["hero_troop_count"]
            if defend_group[block].get("troop"):
                defender_deads[block]["user_troop"] = defend_group[block]["troop"]
                defender_deads[block]["deads"] += defend_group[block]["count"]
                attacker_statistic.kill += defend_group[block]["count"]
                defender_statistic.dead += defend_group[block]["count"]
            defend_group.pop(block)
        attacker_got_damage = rest_defend_damage / a_d_ratio    
        for block in attack_unmatch:
            attacker_block_got_damage = attacker_got_damage * (attack_group[block]["total_attack_health"] / rest_attack_health)
            if attack_group[block].get("troop") and attack_group[block].get("hero"):
                user_hero = attack_group[block]["hero"]
                hero_damage_ratio = user_hero.current_health / attacker_block_got_damage
                hero_got_damage = attacker_block_got_damage * hero_damage_ratio
                if attack_group[block].get("hero_troop"):
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if (hero_got_damage / summon_health_per_troop) > attack_group[block]["hero_troop_count"]:
                        hero_damage_left = hero_got_damage - (summon_health_per_troop * attack_group[block]["hero_troop_count"])
                        attacker_statistic.dead += attack_group[block]["hero_troop_count"]
                        defender_statistic.kill += attack_group[block]["hero_troop_count"]
                        attacker_deads[block]["hero_troop_deads"] += attack_group[block]["hero_troop_count"]
                        attack_group[block]["hero_troop_count"] = 0
                        user_hero.current_health -= round(hero_damage_left)
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        attacker_statistic.dead += lost_troops
                        defender_statistic.kill += lost_troops
                        attacker_deads[block]["hero_troop_deads"] += lost_troops
                        attack_group[block]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()
                attacker_troop_got_damage = (1-hero_damage_ratio) * attacker_block_got_damage
                lost_troops = math.floor((attacker_troop_got_damage / rest_attack_health) * attack_group[block]["count"])
                attacker_deads[block]["user_troop"] = attack_group[block]["troop"]
                attacker_deads[block]["deads"] += lost_troops
                attacker_statistic.dead += lost_troops
                defender_statistic.kill += lost_troops
                attack_group[block]["count"] -= lost_troops
                attack_group[block]["total_attack_damage"] -= attack_group[block]["total_attack_damage"] * attacker_block_got_damage / attack_group[block]["total_attack_health"]
                attack_group[block]["total_attack_health"] -= attacker_block_got_damage
            elif attack_group[block].get("hero"):
                user_hero = attack_group[block]["hero"]
                if attack_group[block].get("hero_troop"):
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if (attacker_block_got_damage / summon_health_per_troop) > attack_group[block]["hero_troop_count"]:
                        hero_damage_left = attacker_block_got_damage - (summon_health_per_troop * attack_group[block]["hero_troop_count"])
                        attacker_statistic.dead += attack_group[block]["hero_troop_count"]
                        defender_statistic.kill += attack_group[block]["hero_troop_count"]
                        attacker_deads[block]["hero_troop_deads"] += attack_group[block]["hero_troop_count"]
                        attack_group[block]["hero_troop_count"] = 0
                        user_hero.current_health -= round(hero_damage_left)
                        user_hero.save()
                    else:
                        lost_troops = math.floor(attacker_block_got_damage / summon_health_per_troop)
                        attacker_statistic.dead += lost_troops
                        defender_statistic.kill += lost_troops
                        attacker_deads[block]["hero_troop_deads"] += lost_troops
                        attack_group[block]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(attacker_got_damage)
                    user_hero.save()
                attack_group[block]["total_attack_damage"] -= attack_group[block]["total_attack_damage"] * attacker_block_got_damage / attack_group[block]["total_attack_health"]
                attack_group[block]["total_attack_health"] -= attacker_block_got_damage
            elif attack_group[block].get("troop"):
                lost_troops = math.floor((attacker_block_got_damage / rest_attack_health) * attack_group[block]["count"])
                attacker_deads[block]["user_troop"] = attack_group[block]["troop"]
                attacker_deads[block]["deads"] += lost_troops
                attack_group[block]["count"] -= lost_troops
                attack_group[block]["total_attack_damage"] -= attack_group[block]["total_attack_damage"] * attacker_block_got_damage / attack_group[block]["total_attack_health"]
                attack_group[block]["total_attack_health"] -= attacker_block_got_damage
                attacker_statistic.dead += lost_troops
                defender_statistic.kill += lost_troops
            else:
                pass

    else:
        for block in attack_unmatch:
            if attack_group[block].get("hero"):
                user_hero = attack_group[block]["hero"]
                user_hero.is_dead = True
                user_hero.current_health = 0
                user_hero.save()
                attacker_statistic.hero_dead += 1
                defender_statistic.hero_kill += 1
            if attack_group[block].get("hero_troop"):
                attacker_statistic.dead += attack_group[block]["hero_troop_count"]
                defender_statistic.kill += attack_group[block]["hero_troop_count"]
                attacker_deads[block]["hero_troop_deads"] += attack_group[block]["hero_troop_count"]
            if attack_group[block].get("troop"):
                attacker_statistic.dead += attack_group[block]["count"]
                defender_statistic.kill += attack_group[block]["count"]
                attacker_deads[block]["user_troop"] = attack_group[block]["troop"]
                attacker_deads[block]["deads"] += attack_group[block]["count"]
            attack_group.pop(block)
        defender_got_damage = rest_attack_damage / d_a_ratio
        for block in defend_unmatch:
            defender_block_got_damage = defender_got_damage * (defend_group[block]["total_defence_health"] / rest_defend_health)
            if defend_group[block].get("hero") and defend_group[block].get("troop"):
                user_hero = defend_group[block]["hero"]
                hero_damage_ratio = user_hero.current_health / defender_block_got_damage
                hero_got_damage = defender_block_got_damage * hero_damage_ratio
                if defend_group[block].get("hero_troop"):
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if (hero_got_damage / summon_health_per_troop) > attack_group[block]["hero_troop_count"]:
                        hero_damage_left = hero_got_damage - (summon_health_per_troop * attack_group[block]["hero_troop_count"])
                        attacker_statistic.kill += defend_group[block]["hero_troop_count"]
                        defender_statistic.dead += defend_group[block]["hero_troop_count"]
                        defender_deads[block]["hero_troop_deads"] += defend_group[block]["hero_troop_count"]
                        defend_group[block]["hero_troop_count"] = 0
                        user_hero.current_health -= round(hero_damage_left)
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        attacker_statistic.kill += lost_troops
                        defender_statistic.dead += lost_troops
                        defender_deads[block]["hero_troop_deads"] += lost_troops
                        defend_group[block]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()
                defender_troop_got_damage = (1-hero_damage_ratio) * defender_block_got_damage    
                lost_troops = math.floor(defender_troop_got_damage / rest_defend_health * defend_group[block]["count"])
                defender_deads[block]["user_troop"] = defend_group[block]["troop"]
                defender_deads[block]["deads"] += lost_troops
                defend_group[block]["count"] -= lost_troops
                defend_group[block]["total_defence_damage"] -= defend_group[block]["total_defence_damage"] * defender_block_got_damage / defend_group[block]["total_defence_health"]
                defend_group[block]["total_defence_health"] -= defender_block_got_damage
                attacker_statistic.kill += lost_troops
                defender_statistic.dead += lost_troops

            elif defend_group[block].get("hero"):
                user_hero = defend_group[block]["hero"]
                hero_got_damage = defender_block_got_damage
                if defend_group[block].get("hero_troop"):
                    summon_health_per_troop = user_hero.hero.summon_type.health
                    if (hero_got_damage / summon_health_per_troop) > defend_group[block]["hero_troop_count"]:
                        hero_damage_left = hero_got_damage - (summon_health_per_troop * defend_group[block]["hero_troop_count"])
                        attacker_statistic.kill += defend_group[block]["hero_troop_count"]
                        defender_statistic.dead += defend_group[block]["hero_troop_count"]
                        defender_deads[block]["hero_troop_deads"] += defend_group[block]["hero_troop_count"]
                        defend_group[block]["hero_troop_count"] = 0
                        user_hero.current_health -= round(hero_damage_left)
                        user_hero.save()
                    else:
                        lost_troops = math.floor(hero_got_damage / summon_health_per_troop)
                        attacker_statistic.kill += lost_troops
                        defender_statistic.dead += lost_troops
                        defender_deads[block]["hero_troop_deads"] += lost_troops
                        defend_group[block]["hero_troop_count"] -= lost_troops
                else:
                    user_hero.current_health -= round(hero_got_damage)
                    user_hero.save()
                defend_group[block]["total_defence_damage"] -= defend_group[block]["total_defence_damage"] * defender_block_got_damage / defend_group[block]["total_defence_health"]
                defend_group[block]["total_defence_health"] -= defender_block_got_damage


            elif defend_group[block].get("troop"):
                defender_troop_got_damage = defender_block_got_damage    
                lost_troops = math.floor(defender_troop_got_damage / rest_defend_health * defend_group[block]["count"])
                defender_deads[block]["user_troop"] = defend_group[block]["troop"]
                defender_deads[block]["deads"] += lost_troops
                defend_group[block]["count"] -= lost_troops
                defend_group[block]["total_defence_damage"] -= defend_group[block]["total_defence_damage"] * defender_block_got_damage / defend_group[block]["total_defence_health"]
                defend_group[block]["total_defence_health"] -= defender_block_got_damage
                attacker_statistic.kill += lost_troops
                defender_statistic.dead += lost_troops
            else:
                pass

    attacker_statistic.save()
    defender_statistic.save()
    return attack_group, defend_group, attacker_deads, defender_deads


def block_matcher(attack_group, defend_group):
    att_first = [x for x in attack_group.keys() if 10 < x < 15]
    att_second = [x for x in attack_group.keys() if 20 < x < 25]
    att_third = [x for x in attack_group.keys() if 30 < x < 35]
    def_first = [x for x in defend_group.keys() if 10 < x < 15]
    def_second = [x for x in defend_group.keys() if 20 < x < 25]
    def_third = [x for x in defend_group.keys() if 30 < x < 35]
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
        

def block_calculations(attack_match, defend_match, attack_unmatched, defend_unmatched, attack_group, defend_group):
    if attack_match != []:
        for aum, dum in zip(attack_match, defend_match):
            # Attack stats update
            if attack_group[aum].get("troop") and defend_group[dum].get("troop"):
                att_ratio = attack_ratio(attack_group[aum]["troop"], defend_group[dum]["troop"])
            else:
                att_ratio = 1
            troop_crash_bonus = attack_group[aum]["troop"].troop.crash_bonus * attack_group[aum]["count"] if attack_group[aum].get("troop") else 0
            attack_group[aum].update({"temp_attack_damage": attack_group[aum]["total_attack_damage"] * att_ratio + troop_crash_bonus})
            if attack_group[aum].get("hero"):
                hero_crash_bonus = attack_group[aum]["hero"].hero.crash_bonus
                attack_group[aum]["temp_attack_damage"] += hero_crash_bonus
            # Check if archer/siege behind
            try:
                if attack_group[aum+10]["troop"].troop.type == "archer" or attack_group[aum+10]["troop"].troop.type == "siege":
                    if attack_group[aum+10].get("hero"):
                        hero_bonus = hero_attack_bonus(attack_group[aum+10]["hero"], attack_group[aum+10]["troop"])
                    else:
                        hero_bonus = 1
                    att_ratio = attack_ratio(attack_group[aum+10]["troop"], defend_group[dum]["troop"])
                    behind_damage = attack_group[aum+10]["count"] * attack_group[aum+10].attack_level * attack_group[aum+10]["troop"].troop.damage * hero_bonus * att_ratio
                    attack_group[aum]["temp_attack_damage"] += behind_damage
            except:
                pass

            # Defender stats update
            if attack_group[aum].get("troop") and defend_group[dum].get("troop"):
                att_ratio = attack_ratio(defend_group[dum]["troop"], attack_group[aum]["troop"])
            else:
                att_ratio = 1
            troop_crash_bonus = defend_group[dum]["troop"].troop.crash_bonus * defend_group[dum]["count"] if defend_group[dum].get("troop") else 0
            defend_group[dum].update({"temp_defence_damage": defend_group[dum]["total_defence_damage"] * att_ratio + troop_crash_bonus})
            # Check if archer/siege behind
            try:
                dum10 = defend_group[dum+10]
                if dum10["troop"].troop.type == "archer" or dum10["troop"].troop.type == "siege":
                    if dum10.get("hero"):
                        hero_bonus = hero_attack_bonus(dum10["hero"], dum10["troop"])
                    else:
                        hero_bonus = 1
                    att_ratio = attack_ratio(dum10["troop"], attack_group[aum]["troop"])
                    behind_damage = dum10["count"] * dum10["troop"].attack_level * dum10["troop"].troop.damage * hero_bonus * att_ratio
                    defend_group[dum]["temp_defence_damage"] += behind_damage
            except:
                pass


    # Attack stats update
    if attack_unmatched != []:
        for aum in attack_unmatched:
            troop_crash_bonus = attack_group[aum]["troop"].troop.crash_bonus * attack_group[aum]["count"] if attack_group[aum].get("troop") else 0
            attack_group[aum].update({"temp_attack_damage": attack_group[aum]["total_attack_damage"] + troop_crash_bonus})
            # Check if archer/siege behind
            try:
                if attack_group[aum+10]["troop"].troop.type == "archer" or attack_group[aum+10]["troop"].troop.type == "siege":
                    if attack_group[aum+10].get("hero"):
                        hero_bonus = hero_attack_bonus(attack_group[aum+10]["hero"], attack_group[aum+10]["troop"])
                    else:
                        hero_bonus = 1
                    behind_damage = attack_group[aum+10]["count"] * attack_group[aum+10].attack_level * attack_group[aum+10]["troop"].troop.damage * hero_bonus
                    attack_group[aum]["temp_attack_damage"] += behind_damage
            except:
                pass
    
    # defend stats update
    if defend_unmatched != []:
        for dum in defend_unmatched:
            troop_crash_bonus = defend_group[dum]["troop"].troop.crash_bonus * defend_group[dum]["count"] if defend_group[dum].get("troop") else 0
            defend_group[dum].update({"temp_defence_damage": defend_group[dum]["total_defence_damage"]})
            # Check if archer/siege behind
            try:
                dum10 = defend_group[dum+10]
                if dum10["troop"].troop.type == "archer" or dum10["troop"].troop.type == "siege":
                    if dum10.get("hero"):
                        hero_bonus = hero_attack_bonus(dum10["hero"], dum10["troop"])
                    else:
                        hero_bonus = 1
                    behind_damage = dum10["count"] * dum10["troop"].attack_level * dum10["troop"].troop.damage * hero_bonus
                    defend_group[dum]["temp_defence_damage"] += behind_damage
            except:
                pass

    return attack_group, defend_group




                    