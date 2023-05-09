from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, CreateView, TemplateView, DetailView
from .models import Alliances, AllianceMembers, AllianceJoinRequest, AllianceChats, AllianceDepartingCampaign, AllianceDepartingHeroes
from main.models import UserTroops, UserHeroes, Location
from battle.models import Battles
from accounts.models import Profile
from .forms import AllianceCreateForm
from .campaign_management import AllianceCampaignManagement
from django.contrib.auth.decorators import login_required
from main.models import Notifications
import json


# Create your views here.



class AllianceListView(LoginRequiredMixin, ListView):
    model = Alliances
    template_name = "alliances/alliances.html"
    context_object_name = "alliances"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        have_alliance = True if AllianceMembers.objects.filter(member=self.request.user).exists() else False
        context["have_alliance"] = have_alliance
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context
    




class AllianceCreateView(LoginRequiredMixin, CreateView):
    model = Alliances
    form_class = AllianceCreateForm
    # fields = ["name", "description", "banner"]
    template_name = "alliances/create_alliance.html"
    success_url = reverse_lazy('alliances: alliance_create')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banner_range = range(1,37)
        context["banner_range"] = banner_range
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify

        return context
    
    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()

        name_check, name_message = self.check_ally_name_available(form_data)
        banner_check, banner_message = self.banner_check(form_data)

        if name_check and not self.check_user_has_ally() and banner_check:
            ally = Alliances.objects.create(
                name = form_data["name"],
                description = form_data["description"],
                founder = self.request.user,
                banner = form_data["banner-choice"]
            )
            AllianceMembers.objects.create(
                alliance = ally,
                member = self.request.user,
                role = 'founder'
            )
            profile = Profile.objects.get(user=self.request.user)
            profile.alliance = ally
            profile.save()
            messages.add_message(request, messages.SUCCESS, f"A new alliance is created")
            return redirect("/alliances")

        elif not name_check:
            messages.add_message(request, messages.SUCCESS, name_message)
            return redirect("/alliances/create")
        
        elif not banner_check:
            messages.add_message(request, messages.SUCCESS, banner_message)
            return redirect("/alliances/create")
        
        else:
            messages.add_message(request, messages.WARNING, "Something is wrong")
            return redirect ("/alliances")
    

    def check_ally_name_available(self, form_data):
        ally_names = [ally.name for ally in Alliances.objects.all()]
        if form_data["name"] in ally_names:
            return False, "This name is already taken."
        else:
            return True, "OK"
        
    def check_user_has_ally(self):
        user = self.request.user
        if Profile.objects.get(user = user).alliance:
            return True
        else:
            return False
        
    def banner_check(self, form_data):
        banners_taken = [ally.banner for ally in Alliances.objects.all()]
        if form_data["banner-choice"] in banners_taken:
            return False, "This banner is taken!"
        else:
            return True, ""


class AllianceUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'alliances/alliance_update.html'

    def get(self, request, *args, **kwargs):
        if Alliances.objects.filter(founder = self.request.user).exists():
            context = self.get_context_data(**kwargs)
            alliance = Alliances.objects.get(founder=self.request.user)
            context["alliance"] = alliance

            banner_range = range(1,37)
            context["banner_range"] = banner_range
            return self.render_to_response(context)
        else:
            return redirect('/alliances')
    

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()

        banner_check, banner_message = self.banner_check(form_data)
        if banner_check:
            alliance = Alliances.objects.get(founder = self.request.user)
            alliance.description = form_data["description"]
            alliance.banner = form_data["banner-choice"]
            alliance.save()
            messages.add_message(request, messages.SUCCESS, "Alliance is updated.")
            return redirect('/alliances')
        else:
            messages.add_message(request, messages.WARNING, "Banner is taken!")
            return redirect('/alliances')
        
        
    def banner_check(self, form_data):
        banners_taken = [ally.banner for ally in Alliances.objects.all()]
        if form_data["banner-choice"] in banners_taken:
            return False, "This banner is taken!"
        else:
            return True, ""
    

class AllianceDetailView(LoginRequiredMixin, DetailView):
    model = Alliances
    template_name = "alliances/alliance_detail.html"
    context_object_name = "alliance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_sent = True if AllianceJoinRequest.objects.filter(alliance = self.get_object(), requester = self.request.user) else False
        context["request_sent"] = request_sent

        have_alliance = True if AllianceMembers.objects.filter(member=self.request.user).exists() else False
        context["have_alliance"] = have_alliance
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context


    def post(self, request, *args, **kwargs):

        if self.alliance_side_check() and not AllianceMembers.objects.filter(member=self.request.user).exists():
            AllianceJoinRequest.objects.create(
                alliance = self.get_object(),
                requester = self.request.user
            )
            messages.add_message(request, messages.SUCCESS, "Request has sent!")
        else:
            messages.add_message(request, messages.WARNING, "You are looking for your fortune in wrong side !")
        return redirect(f'/alliances/{kwargs["pk"]}')


    def alliance_side_check(self):
        user_side = Profile.objects.get(user=self.request.user).side
        if user_side == self.get_object().side:
            return True
        else:
            return False
    



class MyAllyView(LoginRequiredMixin, TemplateView):
    template_name = "alliances/my_ally.html"

    def get(self, request, *args, **kwargs):
        my_alliance = AllianceMembers.objects.filter(member = self.request.user)
        if my_alliance.exists():
            context = self.get_context_data(**kwargs)
            # Alliance object
            alliance = my_alliance.get().alliance
            context["alliance"] = alliance

            # Join Request
            if my_alliance.get().role == "admin" or my_alliance.get().role == 'founder':
                join_requests = AllianceJoinRequest.objects.filter(alliance = alliance)
            else:
                join_requests = None
            
            # Last 20 Chat messages
            last_chats = AllianceChats.objects.filter(alliance = alliance).order_by('time')
            length = len(last_chats)
            length -= 20 if length > 20 else length
            last_chats = last_chats[length:]



            # GET MEMBERS
            alliance_members = AllianceMembers.objects.filter(alliance=alliance)
            alliance_members_users = [member.member for member in alliance_members]
            # GET LAST 5 BATTLE
            last_battles_attack = Battles.objects.filter(Q(attacker__in = alliance_members_users)).order_by('-id')[:5]
            last_battles_defend = Battles.objects.filter(Q(defender__in = alliance_members_users)).order_by('-id')[:5]

            # GET ALLIANCE CAMPAIGN
            alliance_campaigns = AllianceDepartingCampaign.objects.filter(alliance=alliance)

            # self user role
            user_role = my_alliance.get(member = self.request.user).role

            

            context["join_requests"] = join_requests

            context["last_chats"] = last_chats
            context["user_id"] = self.request.user.id
            context["alliance_members"] = alliance_members
            context["last_battles_attack"] = last_battles_attack
            context["last_battles_defend"] = last_battles_defend
            context["alliance_campaigns"] = alliance_campaigns
            context["user_role"] = user_role
            notify = Notifications.objects.get(user = self.request.user)
            notify.alliance = False
            notify.save()
            context["notify"] = notify
            
            return self.render_to_response(context)


        else:
            return redirect('/alliances')
    

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        user = self.request.user
        alliance_member = AllianceMembers.objects.get(member = user)
        alliance = alliance_member.alliance


        if 'send-message' in form_data:
            my_alliance = AllianceMembers.objects.get(member = self.request.user)
            AllianceChats.objects.create(
                alliance = alliance,
                sender = user,
                message = form_data['message']
            )

        elif 'request-handle' in form_data:
            req_id = int(form_data['request-handle'])
            join_request = AllianceJoinRequest.objects.get(id=req_id)

            if form_data['decision'] == 'True' and join_request.alliance == alliance and (alliance_member.role in ["admin", "founder"]):
                AllianceMembers.objects.create(
                    alliance = alliance,
                    member = join_request.requester
                )
                messages.add_message(request, messages.SUCCESS, f"{join_request.requester} has join the alliance")
                join_request.delete()
            elif form_data['decision'] == 'False' and join_request.alliance == alliance and (alliance_member.role in ["admin", "founder"]):
                join_request.delete()
            else:
                return redirect('/no-auth')
            
        elif form_data["form_type"] == "delete-campaign":
            campaign = AllianceDepartingCampaign.objects.get(id = int(form_data["id"]))
            auth_roles = ["founder", "admin"]
            if alliance_member.role in auth_roles or campaign.creator_user == alliance_member:
                alliance_campaign_management = AllianceCampaignManagement(form_data, self.request.user, alliance_member)
                alliance_campaign_management.cancel_campaign(campaign)
                messages.add_message(request, messages.WARNING, "Campaign has been deleted! Troops are back to home.")
                return redirect('/alliances/my_ally')
            else:
                messages.add_message(request, messages.WARNING, "Only creator, admin or founder can delete the campaign!")
                return redirect('/alliances/my_ally')
        
        elif form_data["form_type"] == "member_role_form":
            print(form_data)
            auth_roles = ["founder", "admin"]
            filtered_data = {k[7:]:v for k,v in form_data.items() if k.startswith("member")}
            print(filtered_data)
            if alliance_member.role not in auth_roles:
                messages.add_message(request, messages.WARNING, "You do not have auth to do this. Only admin or founder role can do it")
                return redirect('/no-auth')
            elif "founder" not in filtered_data.values() or "admin" not in filtered_data.values():
                messages.add_message(request, messages.ERROR, "There should be at least one admin or founder in alliance")
            else:
                all_member = AllianceMembers.objects.filter(alliance=alliance)
                for id, role in filtered_data.items():
                    member = all_member.get(id = int(id))
                    if member.role == role:
                        pass
                    else:
                        member.role = role
                        member.save()
                messages.add_message(request, messages.SUCCESS, "Saved.")


            return redirect('/alliances/my_ally')
        
        elif form_data["form_type"] == "leave-ally":
            alliance_member.delete()
            messages.add_message(request, messages.SUCCESS, "You left the alliance")
            return redirect('/alliances')
        else:
            return redirect('alliances/my_ally')


            

        

        return redirect('/alliances/my_ally')
    


class NewAllyCampaign(LoginRequiredMixin, TemplateView):
    template_name = "alliances/new_campaign.html"

    def get(self, request, *args, **kwargs):
        my_alliance = AllianceMembers.objects.filter(member = self.request.user)
        if my_alliance.exists():
            context = self.get_context_data(**kwargs)

            # context is here
            user_troops = UserTroops.objects.filter(user = self.request.user).order_by('id')
            user_heroes = UserHeroes.objects.filter(user=self.request.user)

            # positions
            positions = ["11","12","13","14","21","22","23","24","31","32","33","34"]

            # All location data
            locations = Location.objects.all()
            location_data = dict()

            for obj in locations:
                location_data.update(
                    {f"{obj.locx},{obj.locy}": f"{obj.user} | {obj.location_name}"}
                )
            
            location_data = json.dumps(location_data)



            context["user_troops"] = user_troops
            context["user_heroes"] = user_heroes
            context["positions"] = positions
            context["location_data"] = location_data
            notify = Notifications.objects.get(user = self.request.user)
            context["notify"] = notify
            return self.render_to_response(context)


        else:
            return redirect('/alliances')
        
    
    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        print(form_data)
        alliance_member = AllianceMembers.objects.get(member = self.request.user)
        alliance_campaign_management = AllianceCampaignManagement(form_data, self.request.user, alliance_member)

        message = alliance_campaign_management.create_alliance_campaign()
        messages.add_message(request, messages.SUCCESS, message)
       
        
        return redirect('/alliances/my_ally')


class AllyCampaignDetailView(LoginRequiredMixin, DetailView):
    model = AllianceDepartingCampaign
    template_name = "alliances/alliance_campaign_detail.html"
    context_object_name = "alliance_campaign"

    def get(self, request, *args, **kwargs):
        try:
            user_alliance = AllianceMembers.objects.get(member = self.request.user).alliance

            if self.get_object().alliance != user_alliance:
                return redirect('/no-auth')
            else:
                return super().get(request, *args, **kwargs)
        except:
            return redirect('/no-auth')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_troops = UserTroops.objects.filter(user= user)
        user_heroes = UserHeroes.objects.filter(user=user)

        positions = ["11","12","13","14","21","22","23","24","31","32","33","34"]
        campaign_data = dict()
        campaign = self.get_object()
        for pos in positions:
            troop = campaign.group.get(position = int(pos)).user_troop
            count = campaign.group.get(position = int(pos)).count

            try:
                hero = campaign.heroes.get(position = int(pos)).user_hero
            except:
                hero = None
            campaign_data.update(
        {pos : {"available": False if any([troop, hero]) else True, "user_troop": troop, "hero": hero, "count": count}}
            )


        context["user_troops"] = user_troops
        context["user_heroes"] = user_heroes
        context["campaign_data"] = campaign_data
        notify = Notifications.objects.get(user = user)
        context["notify"] = notify
        return context
    

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        alliance_campaign = AllianceDepartingCampaign.objects.get(id= self.kwargs["pk"])
        
        alliance_member = AllianceMembers.objects.get(member = self.request.user)

        if alliance_member.member != self.request.user:
            return redirect('/no-auth')
        
        elif form_data["form_type"] == "alliance_campaign_save":

            alliance_campaign_management = AllianceCampaignManagement(form_data, self.request.user, alliance_member)
            message = alliance_campaign_management.save_alliance_campaign(alliance_campaign)
            messages.add_message(request, messages.SUCCESS, message)

            return redirect(f'/alliances/campaign/{self.kwargs["pk"]}')
        
        elif form_data["form_type"] == "alliance_campaign_send":
            alliance_campaign_management = AllianceCampaignManagement(form_data, self.request.user, alliance_member)

            if alliance_campaign.creator_user.member == self.request.user:
                check = alliance_campaign_management.send_alliance_campaign(alliance_campaign)
                if check:
                    alliance_campaign_management.delete_alliance_campaign(alliance_campaign)
                    messages.add_message(request, messages.SUCCESS, "Campaign has sent !")
                    return redirect('/alliances/my_ally')
                else:
                    messages.add_message(request, messages.SUCCESS, "An Error Accured ! Please get in touch with the admin")

                    return redirect(f'/alliances/campaign/{self.kwargs["pk"]}')
            else:
                return redirect('/no-auth')

        else:
            return redirect(f'/alliances/campaign/{self.kwargs["pk"]}')


@login_required
def cancel_campaign_troop_view(request, campaign_id, position):
    try:
        user = request.user
        campaign = AllianceDepartingCampaign.objects.get(id = campaign_id)
        troop_section = campaign.group.get(position=position)
        if troop_section.user_troop.user == user:
            cancel_campaign_troop(campaign, position)
            messages.add_message(request, messages.SUCCESS, "Success.")
            return redirect(f'/alliances/campaign/{campaign_id}')
        else:
            return redirect('/no-auth')

    except:
        return redirect(f'/alliances/campaign/{campaign_id}')

@login_required
def kick_user(request, alliance_id, member_id):
    try:    
        member = AllianceMembers.objects.get(id = member_id)
        ally_user = AllianceMembers.objects.get(member=request.user)
        if ally_user.alliance.id == alliance_id and (ally_user.role == 'founder' or ally_user.role == 'admin'):
            member.delete()
            messages.add_message(request, messages.SUCCESS, f"{member} has kicked.")
            return redirect('/alliances/my_ally')
        else:
            return redirect('/no-auth')
    except:
        return redirect('/no-auth')

# Cancel a troop

def cancel_campaign_troop(alliance_campaign, position):
    campaign_troop_obj = alliance_campaign.group.get(position=position)
    departing_hero = AllianceDepartingHeroes.objects.filter(position=position)
    if campaign_troop_obj.user_troop:
        campaign_troop_obj.user_troop.count += campaign_troop_obj.count
        campaign_troop_obj.user_troop.save()
        campaign_troop_obj.user_troop = None
        campaign_troop_obj.count = 0
        campaign_troop_obj.save()

    if departing_hero.exists():
        hero = departing_hero.get(position=position)
        hero.user_hero.is_home = True
        hero.user_hero.save()
        hero.delete()

    else:
        pass