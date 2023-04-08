from datetime import timedelta
from django.shortcuts import  redirect, render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from .models import Resources, UserBuildings, UserTroops, Troops, UserTracker, Messages, Settlement, Buildings, Race, UserTroopTraining, TroopUpgrades, Profile
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import math
from django.db.models import Sum
from .heroes import HeroManagement
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
        user = self.request.user
        context['user_id'] = user.id
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
        resource_prod = resource_production(user)

        resource_buildings = UserBuildings.objects.filter(Q(user=self.request.user) & (Q(building__type="wood") | Q(building__type="stone") | Q(building__type="iron") | Q(building__type="grain"))).order_by("building")
        context["resource_buildings"] = resource_buildings
        
        builders = UserTroops.objects.get(user=user, troop__name="Builder")
        context["builders"] = builders
        context.update(resource_prod)

        context["resources"] = resources
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


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'main/profile.html'
    context_object_name = 'profile'


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

        places = Settlement.objects.filter(user=self.request.user).order_by('settlement_id')
        context["places"] = places
        return context
    




@login_required
def building_view(request, settlement_id):
    user = request.user
    place = Settlement.objects.get(user=user, settlement_id = settlement_id)
    if not place.building:
        print("YOHHHH")
        print("EXCEPT ÇALIŞTI")
        return redirect(f'/new_building/{settlement_id}')
    
    
    building = UserBuildings.objects.get(id = place.building.id)
    if building.building.name == "Fortress":
        return redirect(f"/fortress/{settlement_id}")
    troops = UserTroops.objects.filter(user=user, troop__building__id = place.building.building.id).order_by('troop_id')

    if place.building.building.type == "armory":
        return redirect(f"/armory/{settlement_id}")

    
    if request.method == "GET":
        tracker = UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        troops = UserTroops.objects.filter()
        # troops= troop_training_check(troops, building)
        # trainings= UserTroopTraining.objects.filter(user=user, user_building = building)
        trainings= building_units(building)

        builder = UserTroops.objects.get(user=user, troop__name = "Builder")
        context = {"building": building, "troops": troops, "builder": builder}
        context["builder_iterator"] = range(1,builder.count+1)
        context["settlement_id"] = settlement_id
        context["trainings"] = trainings
        return render(request, "main/building.html", context)

    elif request.method == "POST":
        resources = Resources.objects.get(user=user)
        buildings_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('worker'))['worker__sum']
        

        for troop in troops:
            if str(troop.troop.id) in request.POST.keys():
                form_data = int(request.POST[str(troop.troop.id)])

                if all((resources.wood > form_data * troop.troop.wood, resources.stone > form_data * troop.troop.stone, resources.iron > form_data * troop.troop.iron, resources.grain > form_data * troop.troop.grain)) and troop.troop.prerequisite <= building.level:

                    # CHECKS TOTAL BUILDER NUMBER, 100 MAX.
                    resource_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('resource_worker'))['resource_worker__sum']
                    builder_training = UserTroopTraining.objects.get(user=user, troop__name="Builder")
                    if troop.troop.name == "Builder" and (troop.count + buildings_worker + resource_worker + builder_training.training + form_data > 100):
                        messages.add_message(request, messages.WARNING, f"You can not train more than 100 Builders. You currently have {troop.count + buildings_worker+builder_training.training+resource_worker} builder. You can train {100 - (troop.count + buildings_worker + builder_training.training + resource_worker)} more builder.")
                        return redirect(f"/building/{settlement_id}")

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
    settlement = Settlement.objects.get(user=user, settlement_id = settlement_id)
    try:
        building = settlement.building
    except:
        building = UserBuildings.objects.get(user=user, building__name = "Fortress")
    
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
        
    return redirect(f"/building/{settlement_id}/")


@login_required
def resource_builder_update_view(request, resource_type):
    user=request.user
    
    if request.method == "GET":
        #SEND SIGNAL FIRST ALWAYS      
        tracker = UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        building = UserBuildings.objects.get(user=user, building__type = resource_type)
        builder = UserTroops.objects.get(user=user, troop__name="Builder")

        #GET the current production
        resources = resource_production(user)
        resources = resources[resource_type]

        context = {"building": building, "builder": builder}
        context["resources"] = resources
        # Available builders
        context["available"] = building.worker + builder.count
        return render(request, "main/resource_builder_update.html", context)
    
    elif request.method == "POST":
        try:
            form = int(request.POST["builder-update"])
        except:
            form = 0
        building = UserBuildings.objects.get(user=user, building__type = resource_type)
        builder = UserTroops.objects.get(user=user, troop__name="Builder")
        if form <= building.worker + builder.count:
            total_builder = building.worker + builder.count
            building.worker = form
            builder.count = total_builder - form
            builder.save()
            building.save()
        else:
            messages.add_message(request, messages.WARNING, "Not enough builder.")

        return redirect(f"/resource/{resource_type}")
    else:
        return redirect("/")


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

        return render(request, f"main/new_building.html", context)
    
    elif request.method == "POST":
        try:
            builder_no = int(request.POST["builder"])
        except:
            # A stupid but working solution
            builder_no = 99999
        building_no = int(request.POST["building"])

        resources = Resources.objects.get(user=request.user)
        building = Buildings.objects.get(id=building_no)
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

        return render(request, "main/armory.html", context)
    
    else:
        upgrade = TroopUpgrades.objects.get(user=request.user)
        armory = UserBuildings.objects.get(user=request.user, building__type = "armory")
        print(armory)
        print(armory.level)
        print(upgrade.banner_carrier)
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


        # EN SON BURDA KALDIK
        # UPgrade olan alanı alacağız. koşulları kontrol edip (mesela time_left sıfır mı, başka upgrade var mı o sırada ?!) time_left ve checkout vereceğiz. resource fln güncellenecek. sonra bir daha signal eklenmesi lazım. bitince usertroop leveli güncellenecek fln. Bir de bina leveli kontrol edilecek. iş çok aq. 


@login_required
def fortress_view(request, settlement_id):
        builder = UserTroops.objects.get(user=request.user, troop__name = "Builder")
        if request.method == "GET":      
            user= request.user

            #User Tracker
            tracker = UserTracker.objects.get(user = user)
            tracker.track += 1
            tracker.save()

            place = Settlement.objects.get(user=user, settlement_id = settlement_id)
            building = UserBuildings.objects.get(id = place.building.id)
            resources = Resources.objects.get(user=user)
            builder_iterator = range(1, builder.count+1)
            trainings= building_units(building)

            hero_management = HeroManagement(request.user)
            hero_management.refresh_heroes_health()
            hero_list = hero_management.hero_market_list()
            user_heroes = hero_management.user_hero_list()

            context = {
                "settlement_id": settlement_id,
                "building": building,
                "builder": builder,
                "builder_iterator": builder_iterator,
                "trainings": trainings,
                "hero_list": hero_list,
                "user_heroes": user_heroes,
                "resources": resources
            }
            return render(request, "main/fortress.html", context)
        
        elif request.method == "POST":
            form_data = request.POST.dict()
            if form_data["form_type"] == "builder_training":
                place = Settlement.objects.get(user=request.user, settlement_id = settlement_id)
                user_building = building = UserBuildings.objects.get(id = place.building.id)
                user_resources = Resources.objects.get(user = request.user)

                check, message, new_training_number = builder_training_check(form_data, request.user, builder, user_resources)
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






            




# Some methods
# calculte the current resource production

def resource_production(user):
    base = 50
    grain_base = 250
    try:
        wood_production = 50
        woods = UserBuildings.objects.filter(user=user, building__type = "wood")
        for wood in woods:
            wood_production += wood.level * 1.25 * wood.resource_worker * base if wood.resource_worker != 0 else wood.level * 1.25 * base
    except:
        wood = base

    try:
        stone_production = 50
        stones = UserBuildings.objects.filter(user=user, building__type = "stone")
        for stone in stones:
            stone_production += stone.level * 1.25 * stone.resource_worker * base if stone.resource_worker != 0 else stone.level * 1.25 * base
    except:
        stone = base
    
    try:
        iron_production = 50
        irons = UserBuildings.objects.filter(user=user, building__type = "iron")
        for iron in irons:
            iron_production += iron.level * 1.25 * iron.resource_worker * base if iron.resource_worker != 0 else iron.level * 1.25 * base
    except:
        iron = base
    
    try:
        grain_production = 250
        grains = UserBuildings.objects.filter(user=user, building__type = "grain")
        for grain in grains:
            grain_production += grain.level * 1.25 * grain.resource_worker * grain_base if grain.resource_worker != 0 else grain.level * 1.25 * grain_base
    except:
        grain= grain_base
        
    # Troops' grain consuption calcutaions
    user_troops = UserTroops.objects.filter(user=user)
    consuption = 0
    for user_troop in user_troops:
        consuption += user_troop.troop.consuption * user_troop.count
    
    grain_production -= consuption

    production = {
        "wood": round(wood_production),
        "stone": round(stone_production),
        "iron": round(iron_production),
        "grain": round(grain_production)
    }
    print(production)
    return production




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
        training.count = UserTroops.objects.get(troop = training.troop).count
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


def builder_training_check(form_data, user, user_builder, user_resources):
    new_training_number = int(form_data[str(user_builder.troop.id)])
    print(f"Training number: {new_training_number}")
    resource_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('resource_worker'))['resource_worker__sum']
    print(f"Resource worker: {resource_worker}")
    builder_training = UserTroopTraining.objects.get(user=user, troop__name="Builder")
    print(f"builder training: {builder_training}")
    buildings_worker = UserBuildings.objects.filter(user=user).aggregate(Sum('worker'))['worker__sum']
    print(f"building worker: {buildings_worker}")

    if all((
        user_resources.wood > new_training_number * user_builder.troop.wood,
        user_resources.stone > new_training_number * user_builder.troop.stone,
        user_resources.iron > new_training_number * user_builder.troop.iron,
        user_resources.grain > new_training_number * user_builder.troop.grain
        )):
  

        if user_builder.count + buildings_worker + resource_worker + builder_training.training + new_training_number > 100:
            message = f"You can not train more than 100 Builders. You currently have {user_builder.count + buildings_worker+builder_training.training+resource_worker} builder. You can train {100 - (user_builder.count + buildings_worker + builder_training.training + resource_worker)} more builder."
            return False, message, 5
        
        else:
            return True, "OK", new_training_number
    else:
        return False, "Not enough resources!", new_training_number

def builder_training(user, user_building, user_builder, user_resources, new_training_number):
    training_center = UserTroopTraining.objects.get(user_building = user_building, troop = user_builder.troop)
    training_center.training += new_training_number
    training_center.save()

    user_resources.wood -= new_training_number * user_builder.troop.wood
    user_resources.stone -= new_training_number * user_builder.troop.stone
    user_resources.iron -= new_training_number * user_builder.troop.iron
    user_resources.grain -= new_training_number * user_builder.troop.grain
    user_resources.save()




# user_builder.count + buildings_worker + builder_training.training + new_training_number < 101