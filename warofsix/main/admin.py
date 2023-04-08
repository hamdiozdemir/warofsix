from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(Race)
# admin.site.register(Mail)
admin.site.register(Market)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "is_selected"]
    list_filter = ["name"]

@admin.register(Troops)
class TroopsAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "race", "type", "damage", "crash_bonus", "building", "prerequisite", "training_time", "speed"]
    list_filter = ("race","type")

@admin.register(Buildings)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "race",  "type", "health", "update_time", "sorting"]
    list_filter = ["race"]


@admin.register(Heroes)
class HeroesAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "race", "token", "health", "damage", "regenerate_time", "summon_type", "summon_amount"]
    list_filter = ["race"]


@admin.register(UserHeroes)
class UserHeroesAdmin(admin.ModelAdmin):
    list_display = ["hero", "user", "is_dead", "is_home", "is_available", "current_health", "regenerate_time_left", "last_checkout"]
    list_filter = ["hero"]


@admin.register(UserTroops)
class UserTroopsAdmin(admin.ModelAdmin):
    list_display = ["user","id", "troop", "count", "defence_level", "attack_level", "training", "last_checkout", "time_passed"]
    list_filter = ["user"]

@admin.register(UserBuildings)
class UserBuildingsAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "building", "level", "worker", "last_checkout", "time_left", "resource_worker"]
    list_filter = ["user"]

@admin.register(UserTroopTraining)
class UserTroopTrainingAdmin(admin.ModelAdmin):
    list_display = ["user", "user_building", "troop", "training", "time_passed", "last_checkout"]

@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ["user", "wood", "stone", "iron", "grain", "token", "last_checkout"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "locx", "locy", "type", "location_name"]
    list_filter = ["type"]

@admin.register(UserTracker)
class UserTrackerAdmin(admin.ModelAdmin):
    list_display = ["user","track"]

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ["sender", "target", "header", "id", "time"]
    list_filter = ["sender"]

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ["user", "total_kill", "total_dead", "hero_kill", "hero_dead"]


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ["user", "building","settlement_id"]


@admin.register(TroopUpgrades)
class TroopUpgradesAdmin(admin.ModelAdmin):
    list_display = ["user", "banner_carrier", "forge_blade", "heavy_armor", "arrow", "upgrading_field", "time_left","last_checkout"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "race", "location", "statistic", "description"]