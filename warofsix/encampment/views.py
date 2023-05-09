from django.shortcuts import redirect
from .models import DepartingCampaigns, ArrivingCampaigns, DefencePosition, ReinforcementTroops
from main.models import UserTroops, Location, UserTracker, Troops, UserHeroes, Notifications
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from .management import TroopManagements
import json


# Create your views here.


class EncampmentListView(LoginRequiredMixin, ListView):
    model = UserTroops
    template_name = "encampment/encampment.html"
    context_object_name = "user_troops"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('troop_id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Tracker eklenebilir sonra........
        track = UserTracker.objects.get(user=self.request.user)
        track.track += 1
        track.save()

        user_heroes = UserHeroes.objects.filter(user=self.request.user)

        arriving_campaigns = ArrivingCampaigns.objects.filter(user=self.request.user)
        arriving_attacks = DepartingCampaigns.objects.filter(target_location__user = self.request.user).exclude(campaign_type = "reinforcement").order_by('arriving_time')

        departing_campaigns = DepartingCampaigns.objects.filter(user=self.request.user)
        departing_reinforcements = departing_campaigns.filter(campaign_type="reinforcement").order_by('arriving_time')
        departing_attacks = departing_campaigns.exclude(campaign_type="reinforcement").order_by('arriving_time')
      
        user_counted_troops = UserTroops.objects.filter(user=self.request.user).exclude(count=0).order_by('troop_id')
        if user_counted_troops.exists():
            context["user_counted_troops"] = user_counted_troops
        else:
            user_counted_troops = UserTroops.objects.filter(user=self.request.user).order_by('troop_id')
            context["user_counted_troops"] = user_counted_troops


        my_loc = Location.objects.get(user=self.request.user)
        reinforcements = ReinforcementTroops.objects.filter(location=my_loc)

        my_reinforcements = ReinforcementTroops.objects.filter(owner = self.request.user)

        user_troops = UserTroops.objects.filter(user=self.request.user)
        user_troops = list(user_troops) + [troop.user_troop for troop in reinforcements] 
        blocks = range(1,13)
        positions = ["11","12","13","14","21","22","23","24","31","32","33","34"]


         # All location data
        locations = Location.objects.all()
        location_data = dict()
        for obj in locations:
            location_data.update(
                {f"{obj.locx},{obj.locy}": f"{obj.user} | {obj.location_name}"}
            )
        location_data = json.dumps(location_data)

        context["reinforcements"] = reinforcements
        context["defensive_formation_data2"] = defensive_formation_data2(self.request.user)
        context["user_heroes"] = user_heroes

        context["union_troops"] = user_troops
        context["blocks"] = blocks
        context["departing_attacks"] = departing_attacks
        context["departing_reinforcements"] = departing_reinforcements
        context["arriving_campaigns"] = arriving_campaigns
        context["positions"] = positions
        context["location_data"] = location_data
        context["arriving_attacks"] = arriving_attacks
        context["my_reinforcements"] = my_reinforcements
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context
    
    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        print(form_data)
        
        troop_management = TroopManagements(form_data, self.request.user)
        if request.POST.get("form_type") == "defence":
            message = troop_management.defence_formation_save()
            messages.add_message(request, messages.SUCCESS, f"{message}")
            return redirect("/encampment")                
        elif request.POST.get("form_type") == "send":
            if form_data["sendType"] == "reinforcement":
                message = troop_management.send_reinforcement()
                messages.add_message(request, messages.WARNING, message)
                return redirect('/encampment')
            message = troop_management.send_troop()
            messages.add_message(request, messages.SUCCESS, f"{message}")   
            return redirect("/encampment")
        
        elif request.POST.get("form_type") == "callback":
            troop_management.reinforcement_callback()
            return redirect("/encampment")
        
        elif request.POST.get("form_type") == "sendback":
            troop_management.reinforcement_sendback()
            return redirect('/encampment')   
        
        else:
            messages.add_message(request, messages.SUCCESS, "Ooopps. Error")
            return redirect("/encampment")   



# DEFENCE FORMATION DATA
# OLD VERSION
def defensive_formation_data(user):
    positions = DefencePosition.objects.filter(user=user)
    defence_data = {
        "troop11": positions.get(position=11).user_troop.troop.id,
        "troop12": positions.get(position=12).user_troop.troop.id,
        "troop13": positions.get(position=13).user_troop.troop.id,
        "troop14": positions.get(position=14).user_troop.troop.id,
        "troop21": positions.get(position=21).user_troop.troop.id,
        "troop22": positions.get(position=22).user_troop.troop.id,
        "troop23": positions.get(position=23).user_troop.troop.id,
        "troop24": positions.get(position=24).user_troop.troop.id,
        "troop31": positions.get(position=31).user_troop.troop.id,
        "troop32": positions.get(position=32).user_troop.troop.id,
        "troop33": positions.get(position=33).user_troop.troop.id,
        "troop34": positions.get(position=34).user_troop.troop.id,
        "numd11": positions.get(position=11).percent,
        "numd12": positions.get(position=12).percent,
        "numd13": positions.get(position=13).percent,
        "numd14": positions.get(position=14).percent,
        "numd21": positions.get(position=21).percent,
        "numd22": positions.get(position=22).percent,
        "numd23": positions.get(position=23).percent,
        "numd24": positions.get(position=24).percent,
        "numd31": positions.get(position=31).percent,
        "numd32": positions.get(position=32).percent,
        "numd33": positions.get(position=33).percent,
        "numd34": positions.get(position=34).percent,
        "countd11": positions.get(position=11).count,
        "countd12": positions.get(position=12).count,
        "countd13": positions.get(position=13).count,
        "countd14": positions.get(position=14).count,
        "countd21": positions.get(position=21).count,
        "countd22": positions.get(position=22).count,
        "countd23": positions.get(position=23).count,
        "countd24": positions.get(position=24).count,
        "countd31": positions.get(position=31).count,
        "countd32": positions.get(position=32).count,
        "countd33": positions.get(position=33).count,
        "countd34": positions.get(position=34).count,

    }
    return defence_data


#NEW VERSION
def defensive_formation_data2(user):
    positions = DefencePosition.objects.filter(user=user)

    defence_data = {
        "31": {
        "troop": positions.get(position=31).user_troop.troop.id,
        "numd": positions.get(position=31).percent,
        "countd": positions.get(position=31).count,
        },
        "32": {
        "troop": positions.get(position=32).user_troop.troop.id,
        "numd": positions.get(position=32).percent,
        "countd": positions.get(position=32).count,
        },
        "33": {
        "troop": positions.get(position=33).user_troop.troop.id,
        "numd": positions.get(position=33).percent,
        "countd": positions.get(position=33).count,
        },
        "34": {
        "troop": positions.get(position=34).user_troop.troop.id,
        "numd": positions.get(position=34).percent,
        "countd": positions.get(position=34).count,
        },
        "21": {
        "troop": positions.get(position=21).user_troop.troop.id,
        "numd": positions.get(position=21).percent,
        "countd": positions.get(position=21).count,
        },
        "22": {
        "troop": positions.get(position=22).user_troop.troop.id,
        "numd": positions.get(position=22).percent,
        "countd": positions.get(position=22).count,
        },
        "23": {
        "troop": positions.get(position=23).user_troop.troop.id,
        "numd": positions.get(position=23).percent,
        "countd": positions.get(position=23).count,
        },
        "24": {
        "troop": positions.get(position=24).user_troop.troop.id,
        "numd": positions.get(position=24).percent,
        "countd": positions.get(position=24).count,
        },
        "11": {
        "troop": positions.get(position=11).user_troop.troop.id,
        "numd": positions.get(position=11).percent,
        "countd": positions.get(position=11).count,
        },
        "12": {
        "troop": positions.get(position=12).user_troop.troop.id,
        "numd": positions.get(position=12).percent,
        "countd": positions.get(position=12).count,
        },
        "13": {
        "troop": positions.get(position=13).user_troop.troop.id,
        "numd": positions.get(position=13).percent,
        "countd": positions.get(position=13).count,
        },
        "14": {
        "troop": positions.get(position=14).user_troop.troop.id,
        "numd": positions.get(position=14).percent,
        "countd": positions.get(position=14).count,
        }
    }
    return defence_data
