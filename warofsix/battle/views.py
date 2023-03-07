from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from encampment.models import DefencePosition, DepartingCampaigns

# Create your views here.


@login_required
def battle_view(request):
    defender = DefencePosition.objects.filter(user=31)
    attacker = DepartingCampaigns.objects.get(id=18)

    defendGrid = position_parser(defender)
    attackGrid = position_parser(attacker.group)



    context = {
        "defendGrid": defendGrid,
        "attackGrid": attackGrid,
        "defender": defender,
        "attacker": attacker
    }

    return render(request, "battle/battle.html", context)





def battle(attack_type, tactic, departing_campaign, defence_position):
    if attack_type == "pillage":
        pass
    
    elif attack_type == "block":
        pass

    elif attack_type == "flank":
        pass

    else:
        raise ValueError("Invalid Input for ATTACK TYPE")



# NOT REQUIRED RIGHT NOW
class BattleGrid:
    def __init__(self):
        self.grid = [[None for j in range(4)] for i in range(3)]


    def set_troops(self, group):
        self.grid[1-1][1-1] = group.get(position=11)
        self.grid[1-1][1-2] = group.get(position=12) 
        self.grid[1-1][1-3] = group.get(position=13) 
        self.grid[1-2][1-1] = group.get(position=21) 
        self.grid[1-2][1-2] = group.get(position=22) 
        self.grid[1-2][1-3] = group.get(position=23) 
        self.grid[1-3][1-1] = group.get(position=31) 
        self.grid[1-3][1-2] = group.get(position=32) 
        self.grid[1-3][1-3] = group.get(position=33) 
        self.grid[1-4][1-1] = group.get(position=41) 
        self.grid[1-4][1-2] = group.get(position=42) 
        self.grid[1-4][1-3] = group.get(position=43) 

    def get_troop(self):
        return self.grid




class BlockBattleGrid:
    def __init__(self, attackGrid, defendGrid):
        self.attackGrid = attackGrid
        self.defendGrid = defendGrid


    def battle_block_one(self):

        for row in range(3):
            for col in range(4):
                attack_troop = self.attack_grid.get_troop[col][row]
                attack_count = attack_troop.count

                defend_troop = self.defence_grid.get_troop[col][row]
                defend_count = defend_troop.count

                battle_attack_ratio = attack_ratio(attack_troop.user_troop, defend_troop.user_troop)
                defend_attack_ratio = attack_ratio(defend_troop.user_troop, attack_troop.user_troop)

                attack_attack_point = attack_count * battle_attack_ratio * attack_troop.user_troop.attack_level
                attack_health = attack_count * attack_troop.user_troop.troop.health * attack_troop.user_troop.defence_level

                defend_attack_point = defend_count * defend_attack_ratio * defend_troop.user_troop.attack_level
                defend_helth = defend_count * defend_troop.user_troop.troop.health * defend_troop.user_troop.defence_level


def position_parser(queryset):
    positions = {
        11: queryset.get(position=11),
        12: queryset.get(position=12),
        13: queryset.get(position=13),
        14: queryset.get(position=14),
        21: queryset.get(position=21),
        22: queryset.get(position=22),
        23: queryset.get(position=23),
        24: queryset.get(position=24),
        31: queryset.get(position=31),
        32: queryset.get(position=32),
        33: queryset.get(position=33),
        34: queryset.get(position=34),
    }
    return positions



def attack_ratio(attacker, defender):
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
    compete = attacker.troop.type + defender.troop.type
    if compete in ratio.keys():
        return ratio[compete]
    else:
        return 1