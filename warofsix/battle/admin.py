from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Battles)
class BattlesAdmin(admin.ModelAdmin):
    list_display = ["id", "attacker", "defender", "auto", "time"]


@admin.register(AttackerDeads)
class AttackerDeadsAdmin(admin.ModelAdmin):
    list_display = ["battle", "position", "status", "user_troop", "troop_count", "deads", "user_hero", "user_hero_troop_count", "user_hero_troop_dead"]


@admin.register(DefenderDeads)
class DefenderDeadsAdmin(admin.ModelAdmin):
    list_display = ["battle", "position", "status", "user_troop", "troop_count", "deads", "user_hero", "user_hero_troop_count", "user_hero_troop_dead"]

@admin.register(DefenderBuildingDemolish)
class DefenderBuildingDemolishAdmin(admin.ModelAdmin):
    list_display = ["battle", "building", "pre_battle_level", "post_battle_level"]

@admin.register(BattlePillageResources)
class BattlePillageResourcesAdmin(admin.ModelAdmin):
    list_display = ["battle", "wood", "stone", "iron", "grain", "rings"]