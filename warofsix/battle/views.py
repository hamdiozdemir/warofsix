from typing import Any, Dict
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from encampment.models import DepartingCampaigns
from .models import Battles
from alliances.models import AllianceMembers
from .simulation import Battle
from main.models import Notifications
from django.db.models import Q

# TESTING VIEW


def battle_task(campaign_id):
    departing_campaign = DepartingCampaigns.objects.get(id=campaign_id)
    battle = Battle(departing_campaign)
    if departing_campaign.campaign_type == "reinforcement":
        pass
    elif departing_campaign.campaign_type == "attackblock":
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.block_battle_fight()

        battle.create_battle_report_objects()
        battle.arriving_create_and_resource_pillage()
        battle.delete_defender_dead_troops()
        # battle.delete_departing_campaign()

    elif departing_campaign.campaign_type == "attackflank":
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.flank_battle_fight()

        battle.create_battle_report_objects()
        battle.arriving_create_and_resource_pillage()
        battle.delete_defender_dead_troops()
        # battle.delete_departing_campaign()
    elif departing_campaign.campaign_type == "pillage":
        attack_group, defend_group, main_attack_group, main_defend_group, attacker_deads, defender_deads = battle.pillage_battle_fight()
        battle.create_battle_report_objects()
        battle.arriving_create_and_resource_pillage()
        battle.delete_defender_dead_troops()
        # battle.delete_departing_campaign()
    else:
        pass


@login_required
def battle_view(request):
    return redirect('/reports')


class BattleReportDetailView(LoginRequiredMixin, DetailView):
    model = Battles
    template_name = "battle/report.html"
    context_object_name = "report"


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.attacker == self.request.user or obj.defender == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        try:
            att_ally = AllianceMembers.objects.get(member=obj.attacker).alliance
        except:
            att_ally = None
        try:
            def_ally = AllianceMembers.objects.get(member=obj.defender).alliance
        except:
            def_ally = None
        
        ally_members = AllianceMembers.objects.filter(Q(alliance=att_ally) | Q(alliance=def_ally))
        auth_allies = [ally_obj.member for ally_obj in ally_members]
        if self.request.user in auth_allies:
            return super().dispatch(request, *args, **kwargs)
        
        else:
            return redirect('/settlement')
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = context["report"]
        defender_positions = [31,32,33,34,21,22,23,24,11,12,13,14]
        defender_data = dict()
        if report.defender != self.request.user and report.is_hidden == True:
            for pos in defender_positions:
                defender_data.update({pos:"?"})
        else:
            for pos in defender_positions:
                defender_data.update({pos: report.defender_group.get(position=pos) if report.defender_group.filter(position=pos).first() else None})

        attacker_positions = [11,12,13,14,21,22,23,24,31,32,33,34]
        attacker_data = dict()
        for pos in attacker_positions:
            attacker_data.update({pos: report.attacker_group.get(position=pos) if report.attacker_group.filter(position=pos).first() else None})

        context["attacker_data"] = attacker_data
        context["defender_data"] = defender_data
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context
        
class BattleReportListView(LoginRequiredMixin, ListView):
    model = Battles
    template_name = "battle/battle_reports.html"
    context_object_name = "reports"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        attacks = Battles.objects.filter(attacker = self.request.user, attacker_is_deleted = False).order_by('-time')
        defends = Battles.objects.filter(defender = self.request.user, defender_is_deleted=False).order_by('-time')
        context["attacks"] = attacks
        context["defends"] = defends
        notify = Notifications.objects.get(user = self.request.user)
        notify.report = False
        notify.save()
        context["notify"] = notify
        return context
    

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        if form_data["form_type"] == "delete_attack_reports":
            deleting_ids = [int(value) for key, value in form_data.items() if key.startswith('delete')]
  
            auth_objects = Battles.objects.filter(attacker=self.request.user)
            for id in deleting_ids:
                try:
                    obj = auth_objects.get(id=id)
                    obj.attacker_is_deleted = True
                    obj.save()
                except:
                    pass
        elif form_data["form_type"] == "delete_defend_reports":
            deleting_ids = [int(value) for key, value in form_data.items() if key.startswith('delete')]

            auth_objects = Battles.objects.filter(defender=self.request.user)
            for id in deleting_ids:
                try:
                    obj = auth_objects.get(id=id)
                    obj.defender_is_deleted = True
                    obj.save()
                except:
                    pass
        else:
            pass



        return redirect('/battle/reports')

# UTILS FUNCS


