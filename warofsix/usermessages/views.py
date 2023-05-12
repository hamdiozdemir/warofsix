from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from main.models import Messages, UserTracker, Notifications, Location, UserTroops
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.db.models import Q
from .forms import MessageCreateForm
from django.contrib import messages
from decouple import config
import random
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.

class UserTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = "You are not authorized to view this page."
    raise_exception = False

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def handle_no_permission(self):
        # Redirect the user to a different page
        return redirect('settlement')



class MessageInboxView(LoginRequiredMixin, ListView):
    model = Messages
    template_name = "usermessages/inbox.html"
    context_object_name = "inbox"

    def get_queryset(self):
        return Messages.objects.filter(target = self.request.user).order_by('-time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notify = Notifications.objects.get(user = self.request.user)
        notify.messages = False
        notify.save()
        context["notify"] = notify
        return context


class MessageSentView(LoginRequiredMixin, ListView):
    model = Messages
    template_name = "usermessages/sent.html"
    context_object_name = "sent"

    def get_queryset(self):
        return Messages.objects.filter(sender = self.request.user).order_by('-time')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        tracker= UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        notify = Notifications.objects.get(user = user)
        context["notify"] = notify
        return context



class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Messages
    template_name = "usermessages/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        return Messages.objects.filter(Q(sender=self.request.user) | Q(target=self.request.user))
    
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        if obj:
            obj.is_read = True
            obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        tracker= UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        return context

    

class MessageCreateView(LoginRequiredMixin, TemplateView):
    template_name = "usermessages/new_message.html"

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        print(data)
        username = data["username"]
        try:
            target_user = User.objects.get(username = username)
        except:
            messages.add_message(request, messages.WARNING, f"Böyle bir kullanıcı bulanamadı{username}")
            return redirect("/usermessages/new_message")
        
        Messages.objects.create(
            sender = self.request.user,
            target = target_user,
            header = data["header"] if data["header"] != "" else "New Message",
            content = data["content"]
        )
        messages.add_message(request, messages.WARNING, f"Message has sent to {target_user}")
        return redirect("/usermessages/inbox")




class AllMessageView(LoginRequiredMixin, TemplateView):
    template_name ="usermessages/all_user_message.html"

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        if data["form_type"] == "all_message":
            key = config("ALL_MESSAGE")
            if data["key"] == key:
                all_trackers = UserTracker.objects.all()
                for tracker in all_trackers:
                    Messages.objects.create(
                        sender = self.request.user,
                        target = tracker.user,
                        header = data["title"],
                        content = data["message"]
                    )
                total = len(all_trackers)
                messages.add_message(request, messages.WARNING, f"Messages has sent to total {total} users.")
            else:
                messages.add_message(request, messages.WARNING, "Forget your key? Please click your ass!")
        
        elif data["form_type"] == "wild_attack":
            key = config("WILD_SEND_PASS")
            if key == data["wild-send-key"]:
                user_locations = Location.objects.filter(user__isnull=False ,type="settlement")
                target_user_location = random.choice(user_locations)

                wildling_location = random.choice(Location.objects.filter(user__isnull=False, type="wild"))
                
                from encampment.models import DepartingCampaigns, DepartingTroops
                from main.wild import WildUpdates
                wild_user = wildling_location.user
                wild_update = WildUpdates(wild_user)
                wild_update.troop_update()

                campaign = DepartingCampaigns.objects.create(
                    user = wildling_location.user,
                    main_location = wildling_location,
                    target_location = target_user_location,
                    campaign_type = "pillage",
                    arriving_time = timezone.now()
                )
                wild_troops = UserTroops.objects.filter(user=wildling_location.user).first()

                for position in [11,12,13,14,21,22,23,24,31,32,33,34]:
                    DepartingTroops.objects.create(
                        user = wildling_location.user,
                        position = position,
                        user_troop = wild_troops,
                        count = wild_troops.count if position == 11 else 0,
                        campaign = campaign
                    )
                campaign.time_left = round(campaign.distance / campaign.speed * 3600)
                campaign.arriving_time = timezone.now() + timedelta(seconds=campaign.time_left)
                campaign.save()
                wild_troops.count = 0
                wild_troops.save()

                from battle.tasks import battle_task
                battle_task.apply_async(args=[campaign.id], countdown = campaign.time_left)
                messages.add_message(request, messages.WARNING, f"From {wildling_location.user} to {target_user_location.user} has created! hhahahahhaha")
            else:
                messages.add_message(request, messages.WARNING, "I will send police to your home dude!")

        elif data["form_type"] == "create_wild_user":
            key = config("WILD_CREATE_PASS")
            if key == data["wild-create-key"]:
                new_user = create_wild_user()
                create_wild_good(new_user, level=data["level"], troop_name=data["troop_name"], range_start=int(data["range_start"]), range_end=int(data["range_end"]), ring_chance=int(data["ring_chance"]))

                messages.add_message(request, messages.WARNING, f"Some new wild is here: {new_user}")
            else:
                return messages.add_message(request, messages.WARNING, "Only thing you have created is: NOTHING !!!")

        return redirect('/usermessages/beacon-of-amon-din')


def create_wild_user():
    from django.contrib.auth.models import User
    from main.models import Race
    number = random.choice(range(99999))
    passw = config("WILD_PASS")
    user = User.objects.create(username=f"wild1{number}", password=passw, is_staff=False, is_active=True, is_superuser=False)
    race = Race.objects.create(user=user, name="Wild", is_selected=True)
    return user

def create_wild_good(user, level, troop_name, range_start, range_end, ring_chance):
    from main.models import Troops, Resources,Statistic, Race, WildData, Notifications
    from accounts.models import Profile
    from encampment.models import DefencePosition
    # create location
    locs = Location.objects.filter(user=None, type="wild")
    loc = random.choice(locs)
    loc.user = user
    loc.save()
    
    # create user troops objects
    troop = Troops.objects.get(name = troop_name)
    troop_count = random.choice(range(range_start, range_end))
    user_troop = UserTroops.objects.create(user=user, troop=troop, count=troop_count)

    # create resources
        # get a lucky choice. make probability 1/4
    ring_number = random.choice(range(ring_chance))
    rings = 1 if ring_number == 1 else 0
    Resources.objects.create(user=user, rings=rings, token=0)

    # statistic
    user_statistic = Statistic.objects.create(user=user)
    race = Race.objects.get(user=user)

    # profile
    Profile.objects.create(
        user = user,
        race = race,
        location = loc,
        statistic = user_statistic,
        description = "Wildlings"
    )

    Notifications.objects.create(user=user)

    # create defensive positions
    positions_list = [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34]
    for pos in positions_list:
        if pos in [11,12,13,14]:
            DefencePosition.objects.create(user=user, position=pos, user_troop=user_troop, percent=25)
        else:
            DefencePosition.objects.create(user=user, position=pos, user_troop=user_troop)
    
    if level == "easy":
        res_prod_number = random.choice(range(500,750))
    elif level == "medium":
        res_prod_number = random.choice(range(1200,2000))
    elif level == "hard":
        res_prod_number = random.choice(range(1200,2000))
    else:
        res_prod_number = random.choice(range(3000, 4500))
    
    WildData.objects.create(user=user, resource_production_number = res_prod_number)

