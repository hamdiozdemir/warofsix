from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Race)
# admin.site.register(Troops)
admin.site.register(Buildings)
# admin.site.register(UserTroops)
admin.site.register(UserBuildings)
admin.site.register(Mail)
admin.site.register(Resources)
admin.site.register(Market)
admin.site.register(Location)

@admin.register(Troops)
class TroopsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "race" ,"health"]
    list_filter = ("race",)


@admin.register(UserTroops)
class UserTroopsAdmin(admin.ModelAdmin):
    list_display = ["user", "troop", "count", "level"]

