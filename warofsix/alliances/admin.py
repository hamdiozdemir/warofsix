from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Alliances)
class AlliancesAdmin(admin.ModelAdmin):
    list_display = ["name", "side", "founder", "size"]
    list_filter = ["side"]


@admin.register(AllianceMembers)
class AllianceMembersAdmin(admin.ModelAdmin):
    list_display = ["alliance", "member", "role"]
    list_filter = ["alliance"]

@admin.register(AllianceJoinRequest)
class AllianceJoinRequestAdmin(admin.ModelAdmin):
    list_display = ["alliance", "requester"]
    list_filter = ["alliance"]


@admin.register(AllianceChats)
class AllianceChatAdmin(admin.ModelAdmin):
    list_display = ["alliance", "sender", "message", "time"]
    list_filter = ["alliance"]


@admin.register(AllianceDepartingCampaign)
class AllianceDepartingsAdmin(admin.ModelAdmin):
    list_display = ["creator_user","id", "target_location", "campaign_type", "time_left","speed", "distance"]


@admin.register(AllianceDepartingTroops)
class AllianceDepartingTroopsAdmin(admin.ModelAdmin):
    list_display = ["position", "user_troop", "count", "campaign"]

@admin.register(AllianceDepartingHeroes)
class AllianceDepartingHeroesAdmin(admin.ModelAdmin):
    list_display = ["position", "user_hero", "campaign"]