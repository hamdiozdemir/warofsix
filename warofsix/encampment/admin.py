from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(DepartingCampaigns)
class DepartingCampaignsAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "campaign_type", "main_location", "target_location", "time_left", "distance", "speed", "auto", "arriving_time"]

@admin.register(DepartingTroops)
class DepartingTroopsAdmin(admin.ModelAdmin):
    list_display = ["user", "position", "user_troop", "count", "campaign_id"]


@admin.register(ArrivingCampaigns)
class ArrivingCampaigns(admin.ModelAdmin):
    list_display = ["user", "id", "campaign_type", "main_location", "target_location", "time_left", "distance", "speed"]

@admin.register(ArrivingTroops)
class ArrivignTroopsAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "user_troop", "count", "campaign"]


@admin.register(ArrivingHeroes)
class ArrivingHearoesAdmin(admin.ModelAdmin):
    list_display = ["campaign", "user_hero"]


@admin.register(DefencePosition)
class DefencePositionAdmin(admin.ModelAdmin):
    list_display = ["user", "position", "user_troop", "percent", "count"]


@admin.register(ReinforcementTroops)
class ReinforcementTroopAdmin(admin.ModelAdmin):
    list_display = ["owner", "location", "user_troop", "count"]

@admin.register(DepartingHeroes)
class DepartingHeroesAdmin(admin.ModelAdmin):
    list_display = ["user", "user_hero", "position", "campaign"]

