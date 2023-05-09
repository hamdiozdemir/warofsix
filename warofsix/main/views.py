from django.shortcuts import  redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Resources, UserBuildings, UserTroops, UserTracker, Settlement, Buildings, Race, UserTroopTraining, TroopUpgrades, UserMarkets, Exchanges, SuperPower, Location, SuperPowerReports, Notifications, MarketSent, Troops, Heroes
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import math
from django.db.models import Sum
from .heroes import HeroManagement
from .superpower import SuperPowerManagement
from accounts.models import Profile
import json
import random


# from main.signals import resource_production



# Create your views here.


# USER auth check for logged in and auth for their dynamic urls
# DOESNT WORK AFTER SOME UPDATES
class UserTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = "You are not authorized to view this page."
    raise_exception = False

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def handle_no_permission(self):
        # Redirect the user to a different page
        return redirect('settlement')


# CBV s

class HomeView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = random.choice(range(1,9))
        from accounts.forms import UserRegistrationForm
        form = UserRegistrationForm()

        context["image"] = image
        context["form"] = form
        return context
    
    def post(self, request, *args, **kwargs):
        print(request.POST.dict())
        data = request.POST.dict() 
        from accounts.forms import UserRegistrationForm
        form = UserRegistrationForm(request.POST)
        races = ["Men", "Dwarves", "Elves", "Isengard","Mordor", "Goblins"]
        if data["race"] in races:
            if form.is_valid():
                new_user = form.save()
                new_user.set_password(form.cleaned_data["password"])
                new_user.save()
                Race.objects.create(user=new_user, name=data["race"], is_selected = True)
        else:
            messages.add_message(request, messages.WARNING, "Choose a valid race pls...")
            return redirect('/')

        return redirect('/accounts/login')
    


class GuideView(TemplateView):
    template_name = "main/guide.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        races = ["Isengard", "Men", "Mordor", "Goblins", "Dwarves", "Elves", "Wild"]
        all_troops = Troops.objects.all()
        troops = dict()
        all_buildings = Buildings.objects.all()
        buildings = dict()
        all_heroes = Heroes.objects.all()
        heroes = dict()
        for race in races:
            troops.update({race: [troop for troop in all_troops.filter(race=race).order_by('building')] }) 
            buildings.update({race: [building for building in all_buildings.filter(race=race).order_by('sorting')] })
            heroes.update({race: [hero for hero in all_heroes.filter(race=race).order_by('rings', 'token')] })
        

        context["troops"] = troops 
        context["buildings"] = buildings 
        context["heroes"] = heroes
        return context
    

    



class ResourcesDetailView(LoginRequiredMixin, DetailView):
    model = Resources
    template_name = "main/resources.html"
    context_object_name = "resources"

    def get_object(self, queryset=None):
        return self.get_queryset().get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)      
        user = self.request.user
        tracker = UserTracker.objects.get(user=self.request.user)
        tracker.track += 1
        tracker.save()
        resources = Resources.objects.get(user=user)

        # get the production per hour
        from .signals import resource_production
        resource_prod = resource_production(user)

        resource_buildings = UserBuildings.objects.filter(Q(user=self.request.user) & (Q(building__type="wood") | Q(building__type="stone") | Q(building__type="iron") | Q(building__type="grain"))).order_by("building")
        context["resource_buildings"] = resource_buildings.order_by('-building__type')
        
        builders = UserTroops.objects.get(user=user, troop__name="Builder")
        context["builders"] = builders
        context.update(resource_prod)

        context["resources"] = resources
        notify = Notifications.objects.get(user = user)
        context["notify"] = notify
        return context
    
    def post(self, request, *args, **kwargs):
        resource_buildings = UserBuildings.objects.filter(Q(building__type="wood") | Q(building__type="stone") | Q(building__type="iron") | Q(building__type="grain"))

        for building in resource_buildings:
            if str(building.id) in request.POST.keys():
                form = request.POST[str(building.id)]
                try:
                    form = int(form)
                except:
                    form = 0
                resource_builder_update(self, self.request.user, building.id, form)
                return redirect("/resources")



class SettlementView(LoginRequiredMixin, ListView):
    model = UserBuildings
    template_name = "main/settlement.html"
    context_object_name = "buildings"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracker = UserTracker.objects.get(user=self.request.user)
        tracker.track += 1
        tracker.save()

        resources = Resources.objects.get(user=self.request.user)
        context["resources"] = resources

        blocks = range(1,37)
        context["blocks"] = blocks
        settle = [
            False,1,False,2,3,False,4,False,False,
            5, False, 6,7,False, 8,9,10,11,
            False, 12, False, False, 13, False, False, 14,15,
            16, False, 17, False, 18, False, 19, False, 20
        ]
        places = Settlement.objects.filter(user=self.request.user)
        settlements = dict()
        for i in range(36):
            if settle[i] == False:
                settlements.update({i+1:False})
            else:
                settlements.update({i+1: places.get(settlement_id = settle[i])})

        

        from encampment.models import DepartingCampaigns, ArrivingCampaigns
        arriving_campaigns = ArrivingCampaigns.objects.filter(user=self.request.user)
        arriving_attacks = DepartingCampaigns.objects.filter(target_location__user = self.request.user).exclude(campaign_type = "reinforcement").order_by('arriving_time')
        
        departing_campaigns = DepartingCampaigns.objects.filter(user=self.request.user)
        departing_reinforcements = departing_campaigns.filter(campaign_type="reinforcement").order_by('arriving_time')
        departing_attacks = departing_campaigns.exclude(campaign_type="reinforcement").order_by('arriving_time')


        context["settlements"] = settlements
        context["places"] = places
        context["settle"] = settle
        context["arriving_campaigns"] = arriving_campaigns
        context["arriving_attacks"] = arriving_attacks
        context["departing_attacks"] = departing_attacks
        context["departing_reinforcements"] = departing_reinforcements

        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context
    


@login_required
def building_view(request, settlement_id):
    user = request.user
    place = get_object_or_404(Settlement, user=user, settlement_id=settlement_id)
    if not place.building:
        return redirect(f'/new_building/{settlement_id}')
    
    
    building = UserBuildings.objects.get(id = place.building.id)
    if building.building.name == "Fortress":
        return redirect(f"/fortress/{settlement_id}")
    troops = UserTroops.objects.filter(user=user, troop__building__id = place.building.building.id).order_by('troop_id')

    if place.building.building.type == "armory":
        return redirect(f"/armory/{settlement_id}")

    if building.building.type == "market":
        return redirect(f"/market/{settlement_id}")

    
    if request.method == "GET":
        tracker = UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        troops = UserTroops.objects.filter()
        trainings= building_units(building)

        builder = UserTroops.objects.get(user=user, troop__name = "Builder")
        context = {"building": building, "troops": troops, "builder": builder}
        context["builder_iterator"] = range(1,builder.count+1)
        context["settlement_id"] = settlement_id
        context["trainings"] = trainings
        notify = Notifications.objects.get(user = user)
        context["notify"] = notify
        return render(request, "main/building.html", context)

    elif request.method == "POST":
        resources = Resources.objects.get(user=user)
        buildings_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('worker'))['worker__sum']
        

        for troop in troops:
            if str(troop.troop.id) in request.POST.keys():
                form_data = int(request.POST[str(troop.troop.id)])

                if all((resources.wood > form_data * troop.troop.wood, resources.stone > form_data * troop.troop.stone, resources.iron > form_data * troop.troop.iron, resources.grain > form_data * troop.troop.grain)) and troop.troop.prerequisite <= building.level:

                    #Training Object
                    training_center = UserTroopTraining.objects.get(user_building=building, troop = troop.troop)
                    training_center.training += int(form_data)
                    training_center.last_checkout = timezone.now()
                    training_center.save()

                    resources.wood -= form_data * troop.troop.wood
                    resources.stone -= form_data * troop.troop.stone
                    resources.iron -= form_data * troop.troop.iron
                    resources.grain -= form_data * troop.troop.grain
                    building.save()
                    troop.save()
                    resources.save()
                else:
                    messages.add_message(request, messages.SUCCESS, 'Not enough resources')
                break
        return redirect(f"/building/{settlement_id}/")

    else:
        return redirect('index')
    

@login_required
def building_update(request, settlement_id, builder):
    user = request.user
    builder = int(builder)
    builder_troop = UserTroops.objects.get(user=user, troop__name = "Builder")
    resources = Resources.objects.get(user=user)
    settlement = get_object_or_404(Settlement, user=user, settlement_id=settlement_id)
    try:
        building = settlement.building
    except:
        building = UserBuildings.objects.filter(user=user, building__name = "Fortress").first()
    
    if all((resources.wood >= building.update_wood, resources.stone >= building.update_stone, resources.iron >= building.update_iron, resources.grain >= building.update_grain)) and building.time_left == 0 and builder_troop.count >= builder and building.level < 21:
        
        building.worker += builder
        builder_troop.count -= builder
        builder_troop.save()
        
        resources.wood -= building.update_wood
        resources.stone -= building.update_stone
        resources.iron -= building.update_iron
        resources.grain -= building.update_grain
        resources.save()
        building.last_checkout = timezone.now()
        building.time_left = building.building.update_time * building.next_level / (building.worker + 1)
        building.save()
    else:
        messages.add_message(request, messages.WARNING, "Not enough resources or currently you are building another one")
        return redirect(f"/building/{settlement_id}/")
        
    return redirect("/settlement")



@login_required
def building_update_cancel(request, settlement_id, action):
    user = request.user
    try:
        settlement = Settlement.objects.get(user=user, settlement_id=settlement_id)
        building = settlement.building
    except:
        return redirect(request, "/")
    if building.time_left != 0:
        # If the building currently updating
        # Set back the resources
        resources = Resources.objects.get(user=user)
        builders = UserTroops.objects.get(user=user, troop__name="Builder")
        resources.wood += building.update_wood
        resources.stone += building.update_stone
        resources.iron += building.update_iron
        resources.grain += building.update_grain
        resources.save()
        # Set back the builders' back
        builders.count += building.worker
        building.worker = 0
        building.time_left = 0
        building.last_checkout = timezone.now()
        building.save()
        builders.save()
        if building.level == 0:
            building.delete()
        messages.add_message(request, messages.SUCCESS, f"{action} successfully. Resources got back.")
        return redirect(f"/building/{settlement_id}")
    else:
        messages.add_message(request, messages.WARNING, f"There is nothing to {action}")
        

@login_required
def new_building(request, settlement_id):
    if request.method== "GET":
        #SEND SIGNAL FIRST ALWAYS      
        tracker = UserTracker.objects.get(user=request.user)
        tracker.track += 1
        tracker.save()

        race = Race.objects.get(user=request.user)
        buildings = Buildings.objects.filter(race=race).order_by("sorting")
        context = {"buildings": buildings}
        builder = UserTroops.objects.get(user=request.user, troop__name = "Builder")
        context["builder"] = builder
        context["builder_iterator"] = range(1,builder.count+1)
        notify = Notifications.objects.get(user = request.user)
        context["notify"] = notify
        return render(request, f"main/new_building.html", context)
    
    elif request.method == "POST":
        try:
            builder_no = int(request.POST["builder"])
        except:
            # A stupid but working solution
            builder_no = 99999
        building_no = int(request.POST["building"])

        resources = Resources.objects.get(user=request.user)
        building = get_object_or_404(Buildings, id=building_no)
        current_builder = UserTroops.objects.get(user=request.user, troop__name="Builder")
        try:
            user_armory_check = UserBuildings.objects.get(user=request.user, building__type="armory" )
        except:
            user_armory_check = False
        if building.type== "armory" and user_armory_check:
            messages.add_message(request, messages.INFO, f"You can not have more than one {user_armory_check.building}")
            return redirect(f"/new_building/{settlement_id}/")

        if all((resources.wood >= building.wood, resources.stone >= building.stone, resources.iron >= building.iron, resources.grain >= building.grain)) and current_builder.count >= builder_no:

            current_builder.count -= builder_no
            resources.wood -= building.wood
            resources.stone -= building.stone
            resources.iron -= building.iron
            resources.grain -= building.grain
            resources.save()
            current_builder.save()

            duration = building.update_time / builder_no

            user_building = UserBuildings.objects.create(user=request.user, building=building, worker=builder_no, last_checkout=timezone.now(), time_left=duration)
            user_building.save()

            if building.name == "Fortress":
                create_super_power(building.race, user_building)


            settle_new = Settlement.objects.get(user=request.user, settlement_id=settlement_id)
            settle_new.building = user_building
            settle_new.save()
            return redirect('/settlement')
        
        else:
            messages.add_message(request, messages.SUCCESS, 'Not enough resources or builders')
            return redirect(f"/new_building/{settlement_id}/")


@login_required
def armory_view(request, settlement_id):

    if request.method == "GET":
        user=request.user
        tracker = UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()

        place = Settlement.objects.get(user=user, settlement_id = settlement_id)
        building = UserBuildings.objects.get(id = place.building.id)
        builder = UserTroops.objects.get(user=user, troop__name = "Builder")
        upgrade = TroopUpgrades.objects.get(user=user)
        
        context = {"building": building, "builder": builder, "upgrade": upgrade}
        context["builder_iterator"] = range(1,builder.count+1)
        context["settlement_id"] = settlement_id
        notify = Notifications.objects.get(user = user)
        context["notify"] = notify
        return render(request, "main/armory.html", context)
    
    else:
        upgrade = TroopUpgrades.objects.get(user=request.user)
        armory = UserBuildings.objects.get(user=request.user, building__type = "armory")
        if upgrade.time_left != 0:
            messages.add_message(request, messages.WARNING, "You re currently upgrading another one.")
            return redirect(f"/armory/{settlement_id}")
        resources = Resources.objects.get(user=request.user)
        if "banner_carrier" in request.POST.keys():
            if all((upgrade.bc_resource <= value for value in (resources.wood, resources.stone, resources.iron, resources.grain))) and armory.level > upgrade.banner_carrier:
                upgrade.time_left = upgrade.bc_duration
                upgrade.last_checkout = timezone.now()
                upgrade.upgrading_field = "banner_carrier"
                upgrade.save()
                resources.wood -= upgrade.bc_resource
                resources.stone -= upgrade.bc_resource
                resources.iron -= upgrade.bc_resource
                resources.grain -= upgrade.bc_resource
                resources.save()
                return redirect(f"/armory/{settlement_id}")
            else:
                messages.add_message(request, messages.WARNING, "Not enough resources or building level")
                return redirect(f"/armory/{settlement_id}")


        elif "forge_blade" in request.POST.keys():
            if all(upgrade.fb_resource <= value for value in (resources.wood, resources.stone, resources.iron, resources.grain)) and armory.level > upgrade.forge_blade:
                upgrade.time_left = upgrade.fb_duration
                upgrade.last_checkout = timezone.now()
                upgrade.upgrading_field = "forge_blade"
                upgrade.save()
                resources.wood -= upgrade.fb_resource
                resources.stone -= upgrade.fb_resource
                resources.iron -= upgrade.fb_resource
                resources.grain -= upgrade.fb_resource
                resources.save()
                return redirect(f"/armory/{settlement_id}")
            else:
                messages.add_message(request, messages.WARNING, "Not enough resources or building level")
                return redirect(f"/armory/{settlement_id}")
 
        elif "heavy_armor" in request.POST.keys():
            if all(upgrade.ha_resource <= value for value in (resources.wood, resources.stone, resources.iron, resources.grain)) and armory.level > upgrade.heavy_armor:
                upgrade.time_left = upgrade.ha_duration
                upgrade.last_checkout = timezone.now()
                upgrade.upgrading_field = "heavy_armor"
                upgrade.save()
                resources.wood -= upgrade.ha_resource
                resources.stone -= upgrade.ha_resource
                resources.iron -= upgrade.ha_resource
                resources.grain -= upgrade.ha_resource
                resources.save()
                return redirect(f"/armory/{settlement_id}")
            else:
                messages.add_message(request, messages.WARNING, "Not enough resources or building level")
                return redirect(f"/armory/{settlement_id}")

        elif "arrow" in request.POST.keys():
            if all(upgrade.fa_resource <= value for value in (resources.wood, resources.stone, resources.iron, resources.grain)) and armory.level > upgrade.arrow:
                upgrade.time_left = upgrade.fa_duration
                upgrade.last_checkout = timezone.now()
                upgrade.upgrading_field = "arrow"
                upgrade.save()
                resources.wood -= upgrade.fa_resource
                resources.stone -= upgrade.fa_resource
                resources.iron -= upgrade.fa_resource
                resources.grain -= upgrade.fa_resource
                resources.save()
                return redirect(f"/armory/{settlement_id}")
            else:
                messages.add_message(request, messages.WARNING, "Not enough resources or building level")
                return redirect(f"/armory/{settlement_id}")
        
        else:
            messages.add_message(request, messages.WARNING, "something went wrong or you re trying something not cool.")
            return redirect(f"/armory/{settlement_id}")



@login_required
def fortress_view(request, settlement_id):
        builder = UserTroops.objects.get(user=request.user, troop__name = "Builder")
        if request.method == "GET":      
            user= request.user

            #User Tracker
            tracker = UserTracker.objects.get(user = user)
            tracker.track += 1
            tracker.save()
            place = get_object_or_404(Settlement, user=user, settlement_id=settlement_id)

            if not place.building.building.name == "Fortress":
                sett = Settlement.objects.filter(user=request.user, building__building__name="Fortress").first()
                return redirect(f'/fortress/{sett.settlement_id}')
            try:
                building = UserBuildings.objects.get(id = place.building.id)
            except:
                return redirect(f'/new_building/{settlement_id}')
            resources = Resources.objects.get(user=user)
            builder_iterator = range(1, builder.count+1)
            trainings= building_units(building)

            hero_management = HeroManagement(request.user)
            hero_management.refresh_heroes_health()
            hero_list, ring_hero, one_ring_hero = hero_management.hero_market_list()
            user_heroes = hero_management.user_hero_list()

            power = SuperPower.objects.get(user_building = building)
            incame_attack = SuperPowerReports.objects.filter(location__user = user).order_by('-id')[:3]
            outgone_attack = SuperPowerReports.objects.filter(super_power = power).order_by('-id')[:3]
            if power.is_active:
                # All location data
                locations = Location.objects.all()
                location_data = dict()

                for obj in locations:
                    location_data.update(
                        {f"{obj.locx},{obj.locy}": f"{obj.user} | {obj.location_name}"}
                    )
                
                location_data = json.dumps(location_data)
            else:
                location_data = None

            context = {
                "settlement_id": settlement_id,
                "building": building,
                "builder": builder,
                "builder_iterator": builder_iterator,
                "trainings": trainings,
                "hero_list": hero_list,
                "ring_hero": ring_hero,
                "one_ring_hero": one_ring_hero,
                "user_heroes": user_heroes,
                "resources": resources,
                "power": power,
                "location_data": location_data,
                "incame_attack": incame_attack,
                "outgone_attack": outgone_attack
            }
            notify = Notifications.objects.get(user = user)
            context["notify"] = notify
            return render(request, "main/fortress.html", context)
        
        elif request.method == "POST":
            form_data = request.POST.dict()
            if form_data["form_type"] == "builder_training":
                place = get_object_or_404(Settlement, user=request.user, settlement_id= settlement_id)
                user_building = building = UserBuildings.objects.get(id = place.building.id)
                user_resources = Resources.objects.get(user = request.user)

                check, message, new_training_number = builder_training_check(form_data, request.user, builder, user_resources, user_building)
                if check:
                    builder_training(request.user, user_building, builder, user_resources, new_training_number)
                    return redirect(f"/fortress/{settlement_id}")
                else:
                    messages.add_message(request, messages.WARNING, message)
                    return redirect(f"/fortress/{settlement_id}")
            
            elif form_data["form_type"] == "hero-buy":
                hero_management = HeroManagement(request.user)
                hero_id = int(form_data["hero_id"])
                message = hero_management.get_hero(hero_id)
                messages.add_message(request, messages.WARNING, message)
                
                return redirect(f"/fortress/{settlement_id}")
            
            elif form_data["form_type"] == "ring-hero-buy":
                hero_management = HeroManagement(request.user)
                hero_id = int(form_data["hero_id"])
                message = hero_management.get_ring_hero(hero_id)
                messages.add_message(request, messages.WARNING, message)
                
                return redirect(f"/fortress/{settlement_id}")
            
            elif form_data["form_type"] == "one-ring-hero-buy":
                hero_management = HeroManagement(request.user)
                hero_id = int(form_data["hero_id"])
                message = hero_management.get_one_ring_hero(hero_id)
                messages.add_message(request, messages.WARNING, message)
                return redirect(f"/fortress/{settlement_id}")

            
            elif form_data["form_type"] == "return-hero":
                hero_management = HeroManagement(request.user)
                message = hero_management.return_hero(int(form_data["hero_id"]))
                messages.add_message(request, messages.WARNING, message)
                return redirect(f"/fortress/{settlement_id}")

            elif form_data["form_type"] == "revival-hero":
                hero_management = HeroManagement(request.user)
                message = hero_management.revival_hero(int(form_data["hero_id"]))
                messages.add_message(request, messages.WARNING, message)
                return redirect(f"/fortress/{settlement_id}")
            
            elif form_data["form_type"] == "refresh-hero":
                hero_management = HeroManagement(request.user)
                hero_management.refresh_heroes_health()
                return redirect(f"/fortress/{settlement_id}")
            
            elif form_data["form_type"] == "power_upgrade":
                print(form_data)
                user_fortress = get_object_or_404(Settlement, user=request.user, settlement_id=settlement_id).building
                power = SuperPowerManagement(request.user, user_fortress.id)
                power.upgrade_super_power()
                return redirect(f"/fortress/{settlement_id}")

            elif form_data["form_type"] == "power_use":
                print(form_data)
                target_location = Location.objects.get(locx = int(form_data["locx"]), locy = int(form_data["locy"]))

                user_fortress = get_object_or_404(Settlement, user=request.user, settlement_id=settlement_id).building
                power = SuperPowerManagement(request.user, user_fortress.id)
                message = power.send_attack(target_location)
                messages.add_message(request, messages.SUCCESS, message)
                                
                return redirect(f"/fortress/{settlement_id}")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong")
                return redirect(f"/fortress/{settlement_id}")




class SuperPowerReportsView(LoginRequiredMixin, DetailView):
    model = SuperPowerReports
    template_name = "main/power_report.html"
    context_object_name = "report"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.super_power.user_building.user == self.request.user or obj.location.user == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/settlement')


@login_required
def market_view(request, settlement_id):

    if request.method == "GET":
        user = request.user
        tracker = UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        settlement = get_object_or_404(Settlement, user=user, settlement_id=settlement_id)
        building = settlement.building
        if not building:
            return redirect(f"/new_building/{settlement_id}")
        
        user_market = UserMarkets.objects.get(user=user)

        exchange_offers = Exchanges.objects.filter(is_complete = False).order_by('-added_time')
        resources = Resources.objects.get(user=user)
        builder = UserTroops.objects.get(user=user, troop__name = "Builder")

        user_offers = Exchanges.objects.filter(offer_user = user, is_complete=False)

        locations = Location.objects.all()
        location_data = dict()
        for obj in locations:
            location_data.update(
                {f"{obj.locx},{obj.locy}": f"{obj.user} | {obj.location_name}"}
            )
        location_data = json.dumps(location_data)


        market_incoming = MarketSent.objects.filter(target_location__user = user, is_complete=False)
        market_outgoing = MarketSent.objects.filter(sender = user, is_complete=False)
  
        context = {
            "user_market": user_market,
            "exchange_offers": exchange_offers,
            "resources" : resources,
            "building" : building,
            "settlement_id": settlement_id,
            "builder_iterator": range(1,builder.count+1),
            "user_offers" : user_offers,
            "location_data": location_data,
            "market_incoming": market_incoming,
            "market_outgoing": market_outgoing
        }
        notify = Notifications.objects.get(user = user)
        context["notify"] = notify
        return render(request, "main/user_market.html", context)
    
    elif request.method == "POST":
        form_data = request.POST.dict()
        if form_data["form_type"] == "new_offer":
            user_resources = Resources.objects.get(user = request.user)
            resource_type = form_data["offer_type"]
            offer_amount = int(form_data["offer_amount"])
            user_current_resource = getattr(user_resources, resource_type, 0)
            # check if user has enough resource
            if user_current_resource >= int(form_data["offer_amount"]):
                market_obj = UserMarkets.objects.get(user=request.user)
                # check if target amount is bigger or less than 2 times
                if offer_amount > 2 * int(form_data["target_amount"]) or offer_amount * 2 < int(form_data["target_amount"]):
                    messages.add_message(request, messages.WARNING, "You can not offer more than 2 times of your type.")
                
                elif offer_amount > market_obj.current:
                    messages.add_message(request, messages.WARNING, "Your offer is over the capacity. You may upgrade your market for more capacity")
                    
                else:
                    Exchanges.objects.create(
                        offer_user = request.user,
                        offer_type = form_data["offer_type"],
                        offer_amount = offer_amount,
                        target_type = form_data["target_type"],
                        target_amount = int(form_data["target_amount"])
                    )

                    setattr(user_resources, resource_type, user_current_resource - offer_amount)
                    user_resources.save()
                    messages.add_message(request, messages.SUCCESS, "Added to Market.")
                    
            else:
                messages.add_message(request, messages.WARNING, "You do not have enough resources !")
        
        
        elif form_data["form_type"] == "send_resources":
            target_loc = get_object_or_404(Location, locx=int(form_data["locx"]), locy=int(form_data["locy"]))
            # target_loc = Location.objects.get(locx=int(form_data["locx"]), locy=int(form_data["locy"]))
            if not target_loc.user and target_loc.type != "settlement":
                messages.add_message(request, messages.WARNING, "There is no place to sent.")
                return redirect(f"/market/{settlement_id}")
            user_loc = Location.objects.get(user = request.user)
            user_market = UserMarkets.objects.get(user = request.user)
            user_resources = Resources.objects.get(user=request.user)
            if not all([
                user_resources.wood >= int(form_data["wood"]),
                user_resources.stone >= int(form_data["stone"]),
                user_resources.iron >= int(form_data["iron"]),
                user_resources.grain >= int(form_data["grain"])
                
            ]):
                messages.add_message(request, messages.WARNING, "Not enough resources")
            
            elif user_market.current < (int(form_data["wood"]) + int(form_data["stone"]) + int(form_data["iron"]) +int(form_data["grain"])):
                messages.add_message(request, messages.WARNING, "Not enough capacity")

            else:
                obj = MarketSent.objects.create(
                    sender = request.user,
                    target_location = target_loc,
                    wood = int(form_data["wood"]),
                    stone = int(form_data["stone"]),
                    iron = int(form_data["iron"]),
                    grain = int(form_data["grain"]),
                    time_left = time_left_calculator(user_loc, target_loc, 20)
                )
                user_resources.wood -= int(form_data["wood"])
                user_resources.stone -= int(form_data["stone"])
                user_resources.iron -= int(form_data["iron"])
                user_resources.grain -= int(form_data["grain"])
                user_resources.save()

                from battle.tasks import resource_send
                resource_send.apply_async(args=[obj.id], countdown=obj.time_left)

                messages.add_message(request, messages.WARNING, f"Resources has sent to {target_loc}")



            return redirect(f"/market/{settlement_id}")
        
        else:
            messages.add_message(request, messages.WARNING, "Some mistakes...")

        return redirect(f"/market/{settlement_id}")


@login_required
def market_accept_offer(request, settlement_id, exchange_id):
    try:
        exchange = Exchanges.objects.get(id = exchange_id)
    except:
        return redirect('/settlement')
    
    # get exchange request & Check if user have resources
    user_resources = Resources.objects.get(user = request.user)
    user_resources_exchange_target = getattr(user_resources, exchange.target_type, 0)
    user_resources_exchange_offer = getattr(user_resources, exchange.offer_type, 0)

    if user_resources_exchange_target >= exchange.target_amount:
        seller_user_resources = Resources.objects.get(user = exchange.offer_user)
        seller_offer = getattr(seller_user_resources, exchange.offer_type, 0)
        seller_target = getattr(seller_user_resources, exchange.target_type, 0)
        setattr(seller_user_resources, exchange.offer_type,seller_offer - exchange.offer_amount)
        setattr(seller_user_resources, exchange.target_type, seller_target + exchange.target_amount)
        seller_user_resources.save()

        setattr(user_resources, exchange.target_type, user_resources_exchange_target - exchange.target_amount)
        setattr(user_resources, exchange.offer_type, user_resources_exchange_offer + exchange.offer_amount)
        user_resources.save()

        exchange.client_user = request.user
        exchange.is_complete = True
        exchange.save()

        messages.add_message(request, messages.SUCCESS, "Exchange complated.")
        return redirect(f"/market/{settlement_id}")

    else:
        messages.add_message(request, messages.WARNING, "You do not have enough resources !")
        return redirect(f"/market/{settlement_id}")



@login_required
def market_cancel_offer(request, settlement_id, exchange_id):
    try:
        exchange = Exchanges.objects.get(id = exchange_id)
        user_resources = Resources.objects.get(user = request.user)
        user_type_resource = getattr(user_resources, exchange.offer_type, 0)
        setattr(user_resources, exchange.offer_type, user_type_resource + exchange.offer_amount)
        user_resources.save()
        exchange.delete()
        messages.add_message(request,messages.SUCCESS, "Offer canceled.")
        return redirect(f"/market/{settlement_id}")
    
    except:
        return redirect('/settlement')




@login_required
def profile_redirect_view(request, user_id):
    try:
        profile = Profile.objects.get(user__id = user_id)
        return redirect(f"/accounts/profile/{profile.id}/")
    except:
        return redirect('/')



def no_auth_view(request):
    return render(request, "main/no_auth.html")


            


# Some methods

# not useful anymore, old version
def troop_training_check(troops, building):
    for troop in troops:
        if troop.training == 0:
            pass
        else:
            time_diff = (timezone.now() - troop.last_checkout).total_seconds()
            training_time = round(troop.troop.training_time / building.level)
            troop.time_passed += round(time_diff)
            trained = math.floor(troop.time_passed / training_time)
            if trained > troop.training:
                trained = troop.training
                troop.time_passed = 0
            
            troop.training -= trained
            troop.count += trained
            troop.time_passed -= trained * training_time
            if troop.time_passed < 0:
                troop.time_passed = 0
            troop.last_checkout = timezone.now()

            troop.time_left_total = timezone.now() + timezone.timedelta(seconds = troop.training * training_time - troop.time_passed)
            troop.time_left_per_troop = training_time - troop.time_passed
 

            troop.save()
    return troops


def training_check(user):
    trainings = UserTroopTraining.objects.filter(user=user)
    for troop in trainings:
        if troop.training == 0:
            troop.time_passed = 0
            troop.save()
        else:
            time_diff = (timezone.now() - troop.last_checkout).total_seconds()
            training_time = round(troop.troop.training_time / troop.user_building.level)
            troop.time_passed += round(time_diff)
            trained = math.floor(troop.time_passed / training_time)
            if trained >= troop.training:
                trained = troop.training
                troop.time_passed = 0
            else:
                troop.time_passed -= trained * training_time
            
            troop.training -= trained
            user_troop = UserTroops.objects.get(user=user, troop=troop.troop)
            user_troop.count += trained
            user_troop.save()

            troop.last_checkout = timezone.now()
            troop.time_left_total = timezone.now() + timezone.timedelta(seconds=troop.training * training_time - troop.time_passed)
            troop.time_left_per_troop = training_time - troop.time_passed

            troop.save()
    return trainings

# SENDS the current trainings and all troops' of user to building_view
def building_units(user_building):
    trainings = UserTroopTraining.objects.filter(user_building=user_building).order_by('troop')
    for training in trainings:
        training.training_time = round(training.troop.training_time / training.user_building.level)
        
        training.time_left_total = timezone.now() + timezone.timedelta(seconds = training.training * training.training_time - training.time_passed)
        training.time_left_per_troop = training.training_time - training.time_passed
        training.count = UserTroops.objects.get(user=user_building.user, troop = training.troop).count
        training.prerequisite = True if training.troop.prerequisite <= user_building.level else False
        training.save()
    return trainings
    


def positive_or_zero(number):
    number = round(number)
    if number < 0:
        number = 0
    return number


def resource_builder_update(self, user, id, value):
    building = UserBuildings.objects.get(id=id)
    builder = UserTroops.objects.get(user=user, troop__name="Builder")

    if value <= building.resource_worker + builder.count:
        total_builder = building.resource_worker + builder.count
        building.resource_worker = value
        builder.count = total_builder - value
        builder.save()
        building.save()
        return messages.add_message(self.request, messages.SUCCESS, f"Updated succesfully")
    else:
        return messages.add_message(self.request, messages.WARNING, f"Not enough builder")


def builder_training_check(form_data, user, user_builder, user_resources,user_building):
    new_training_number = int(form_data[str(user_builder.troop.id)])
    resource_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('resource_worker'))['resource_worker__sum']
    builder_training = 0
    for train in UserTroopTraining.objects.filter(user=user, troop__name="Builder"):
        builder_training += train.training
    buildings_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('worker'))['worker__sum']

    if all((
        user_resources.wood > new_training_number * user_builder.troop.wood,
        user_resources.stone > new_training_number * user_builder.troop.stone,
        user_resources.iron > new_training_number * user_builder.troop.iron,
        user_resources.grain > new_training_number * user_builder.troop.grain
        )):
  

        if user_builder.count + buildings_worker + resource_worker + builder_training + new_training_number > 100:
            message = f"You can not train more than 100 Builders. You currently have {user_builder.count + buildings_worker+builder_training+resource_worker} builder. You can train {100 - (user_builder.count + buildings_worker + builder_training + resource_worker)} more builder."
            return False, message, 5
        
        else:
            return True, "OK", new_training_number
    else:
        return False, "Not enough resources!", new_training_number


def builder_training(user, user_building, user_builder, user_resources, new_training_number):
    training_center = UserTroopTraining.objects.get(user_building = user_building, troop = user_builder.troop)
    training_center.last_checkout = timezone.now()
    training_center.save()
    training_center.training += new_training_number
    training_center.save()

    user_resources.wood -= new_training_number * user_builder.troop.wood
    user_resources.stone -= new_training_number * user_builder.troop.stone
    user_resources.iron -= new_training_number * user_builder.troop.iron
    user_resources.grain -= new_training_number * user_builder.troop.grain
    user_resources.save()


def create_super_power(race, fortress):
    if race == "Men":
        SuperPower.objects.create(
            user_building = fortress,
            name = "Ivory Tower",
            description = "Ivory Tower lets you reveal an enemy's troop's number.",
            power_damage = 0
        )
    elif race == "Elves":
        SuperPower.objects.create(
            user_building = fortress,
            name = "Giant Eagle Strike",
            description = "Giant Eagle Strike lets you make a powerful attack to an enemy's random troops.",
            power_damage = 30000
        )
    elif race == "Dwarves":
        SuperPower.objects.create(
            user_building = fortress,
            name = "The Mighty Catapult",
            description = "The Mighty Catapult lets you make a powerful attack to an enemy's random building.",
            power_damage = 17500
        )
    elif race == "Isengard":
        SuperPower.objects.create(
            user_building = fortress,
            name = "Wizard Tower",
            description = "Wizard Tower lets you make a powerful attack to an enemy's random troops.",
            power_damage = 31000
        )
    elif race == "Mordor":
        SuperPower.objects.create(
            user_building = fortress,
            name = "Gorgoroth Spire",
            description = "The Gorgoroth Spire lets you make a powerful attack to an enemy's random building.",
            power_damage = 18000
        )
    elif race == "Goblins":
        SuperPower.objects.create(
            user_building = fortress,
            name = "Dragon Strike",
            description = "Drogon Strike lets you make a powerful attack to an enemy's random troops.",
            power_damage = 32000
        )
    else:
        pass



def time_left_calculator(main_loc, target_loc, speed):
    x = abs(main_loc.locx - target_loc.locx)
    y = abs(main_loc.locy - target_loc.locy)
    distance = round(((x ** 2) + (y ** 2)) ** 0.5)
    time_left = round(distance / speed * 3600)
    return time_left
