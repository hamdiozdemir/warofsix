from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(Race)
# admin.site.register(Mail)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "is_selected"]
    list_filter = ["name"]

@admin.register(Troops)
class TroopsAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "race", "type", "damage", "health", "crash_bonus", "building", "prerequisite", "training_time", "speed", "burden"]
    list_filter = ("race","type")

@admin.register(Buildings)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "race",  "type", "health", "update_time", "sorting"]
    list_filter = ["race"]


@admin.register(Heroes)
class HeroesAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "race", "token", "rings", "health", "damage", "regenerate_time", "summon_type", "summon_amount"]
    list_filter = ["race"]


@admin.register(UserHeroes)
class UserHeroesAdmin(admin.ModelAdmin):
    list_display = ["hero", "user", "is_dead", "is_home", "status", "current_health", "regenerate_time_left", "last_checkout"]
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
    list_display = ["user", "wood", "stone", "iron", "grain", "token", "rings", "last_checkout"]


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


@admin.register(WildData)
class WildDataAdmin(admin.ModelAdmin):
    list_display = ["user", "resource_production_number", "troop_production_number", "resource_last_checkout", "troop_last_checkout"]


@admin.register(UserMarkets)
class UserMarketAdmin(admin.ModelAdmin):
    list_display = ["user", "offer_capacity", "current"]


@admin.register(Exchanges)
class ExchangesAdmin(admin.ModelAdmin):
    list_display = ["offer_user", "offer_type", "offer_amount", "client_user", "target_type", "target_amount", "is_complete"]


@admin.register(SuperPower)
class SuperPowerAdmin(admin.ModelAdmin):
    list_display = ["user_building", "name", "power_damage", "is_active", "last_checkout", "next_round"]


@admin.register(SuperPowerReports)
class SuperPowerResportsAdmin(admin.ModelAdmin):
    list_display = ["super_power", "location", "building", "troop", "revealed_troop"]


@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "alliance", "report", "messages"]


@admin.register(MarketSent)
class MarketSentAdmin(admin.ModelAdmin):
    list_display = ["sender", "target_location", "wood", "stone", "iron", "grain", "time_left"]