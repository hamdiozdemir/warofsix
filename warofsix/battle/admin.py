from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Battles)
class BattlesAdmin(admin.ModelAdmin):
    list_display = ["attacker", "defender", "auto"]


@admin.register(AttackerDeads)
class AttackerDeadsAdmin(admin.ModelAdmin):
    list_display = ["battle", "troop", "troop", "current", "deads", "alive"]


@admin.register(DefenderDeads)
class DefenderDeadsAdmin(admin.ModelAdmin):
    list_display = ["battle", "troop", "current", "deads", "alive"]