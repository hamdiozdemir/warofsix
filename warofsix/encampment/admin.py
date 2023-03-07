from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(DepartingCampaigns)
class DepartingCampaignsAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "main_location", "target_location", "time_left", "distance", "speed", "auto"]

@admin.register(DepartingTroops)
class DepartingTroopsAdmin(admin.ModelAdmin):
    list_display = ["user", "position", "user_troop", "count", "campaign_id"]


@admin.register(ArrivingCampaigns)
class ArrivingCampaigns(admin.ModelAdmin):
    list_display = ["user", "main_location", "target_location", "time_left", "distance", "speed"]

@admin.register(ArrivingTroops)
class ArrivignTroopsAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "user_troop", "count", "campaign"]


@admin.register(DefencePosition)
class DefencePositionAdmin(admin.ModelAdmin):
    list_display = ["user", "position", "user_troop", "percent", "count"]