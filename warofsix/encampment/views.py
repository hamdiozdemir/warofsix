from django.shortcuts import render, redirect
from .models import DepartingTroops, ArrivingTroops, DepartingCampaigns, ArrivingCampaigns, DefencePosition
from main.models import UserTroops, Location, UserTracker, Troops
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages

from django.views.generic import ListView


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


        departing_groups = list()
        departing_campaigns = DepartingCampaigns.objects.filter(user=self.request.user)
        for dc in departing_campaigns:
            troops = DepartingTroops.objects.filter(campaign = dc).order_by('user_troop_id')
            departing_groups.append((dc, troops))
        
        context["departing_groups"] = departing_groups
        user_counted_troops = UserTroops.objects.filter(user=self.request.user).exclude(count=0).order_by('troop_id')
        if user_counted_troops.exists():
            context["user_counted_troops"] = user_counted_troops
        else:
            user_counted_troops = UserTroops.objects.filter(user=self.request.user).order_by('troop_id')
            context["user_counted_troops"] = user_counted_troops


        percents = [
            (0, "%0"),
            (10, "%10"),
            (20, "%20"),
            (25, "%25"),
            (30, "%30"),
            (40, "%40"),
            (50, "%50"),
            (60, "%60"),
            (70, "%70"),
            (75, "%75"),
            (80, "%80"),
            (90, "%90"),
            (100, "%100")
        ]

        context["percents"] = percents
        context["defensive_formation_data"] = defensive_formation_data(self.request.user)



        return context
    
    def post(self, request, *args, **kwargs):
        
        if request.POST.get("form_type") == "defence":
            print("DEFENCE FORM*********")
            form_data = request.POST.dict()
            print(form_data)
            if defence_formation_percent_check(form_data):
                defence_formation_save(self.request.user, form_data)
                messages.add_message(request, messages.SUCCESS, "Formation updated successfully.")
                return redirect("/encampment")
            else:
                messages.add_message(request, messages.WARNING, "All troop's total percentage should be %100.")
                return redirect("/encampment")
                


        elif request.POST.get("form_type") == "attack":
            form_data = request.POST.dict()
            print(form_data)
            print("ATTACK FORM ---------------")


                # print(form_data)
            # # create the campaing object
            main_location = Location.objects.get(user=self.request.user)
            locx = int(form_data["locx"])
            locy = int(form_data["locy"])
            target_location = Location.objects.get(locx=locx, locy=locy)
            auto = request.POST.get('auto', False) == 'True'
            campaign = DepartingCampaigns.objects.create(user=self.request.user, main_location=main_location, target_location=target_location, auto=auto)

                # #create the departing troops
            positions = [11,12,13,14,21,22,23,24,31,32,33,34]
            for pos in positions:
                user_troop = UserTroops.objects.get(troop__id = form_data["troop"+str(pos)])
                departing_troop = DepartingTroops.objects.create(
                    user=self.request.user,
                    position = pos,
                    user_troop = user_troop,
                    count = int(form_data["num"+str(pos)]),
                    campaign=campaign
                )
                user_troop.count -= int(form_data["num"+str(pos)])
                user_troop.save()
                campaign.time_left = campaign.distance / campaign.speed * 3600
                campaign.save()

                # user_troops = UserTroops.objects.filter(user=self.request.user)
            # for troop in user_troops:
            #     DepartingTroops.objects.create(user=self.request.user, user_troop=troop, count= int(form_data[str(troop.id)]), campaign=campaign)
            #     troop.count -= int(form_data[str(troop.id)])
            #     troop.save()
            # campaign.time_left = campaign.distance / campaign.speed * 3600
            # campaign.save()
   
            return redirect("/encampment")



# SOME FUNCTIONS


# DEFENCE FORMATION DATA

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

    }
    return defence_data


def defence_formation_save(user, data):
    positions = DefencePosition.objects.filter(user=user)
    for pos in positions:
        pos.user_troop = UserTroops.objects.get(troop__id = int(data[f"troop{pos.position}"]))
        pos.percent = int(data[f"numd{pos.position}"])
        pos.save()


def defence_formation_percent_check(data):
    filtered_data = {k:v for k,v in data.items() if k.startswith('troop')}
    new_data = dict.fromkeys(set(filtered_data.values()), 0)
    for k,v in filtered_data.items():
        if v in new_data.keys():
            new_data[v] += int(data["numd"+k[-2:]])
    if all(number == 100 for number in new_data.values()):
        return True
    else:
        return False