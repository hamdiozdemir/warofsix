from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, ListView
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Profile
from main.wild import WildUpdates
from main.models import Notifications
# Create your views here.


# After some changes, adding this redirect func to avoid unexpected 404 error
def accounts_redirect_view(request):
    return redirect('/')

class UserLoginView(LoginView):
    template_name = "login.html"


    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session["user_id"] = self.request.user.id
        return response


def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return redirect('accounts')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile2.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context["profile"]
        if profile.race.name == "Wild":
            from main.models import UserTroops
            wildling = WildUpdates(profile.user)
            wildling.combine_resource_troop_update()
            troops = UserTroops.objects.filter(user=profile.user)
            print(self)
            print(profile.user)
        else:
            troops = None
        context["troops"] = troops
        return context


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile_edit.html"

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user = self.request.user)
            location = profile.location
            context = self.get_context_data(**kwargs)
            context["profile"] = profile
            context["location"] = location
            return self.render_to_response(context)
        except:
            return redirect("/accounts")
    

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        print(form_data)
        if form_data["form_type"] == "profile_edit":
            profile = Profile.objects.get(user = self.request.user)
            location = profile.location
            profile.description = form_data["description"]
            profile.save()

            location.location_name = form_data["location_name"]
            location.save()
            return redirect(f"/accounts/profile/{profile.id}")
            

        else:
            return redirect("/accounts")
    
        
    
class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "accounts/profile_list.html"
    context_object_name = "profiles"


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(race__name="Wild")
        queryset = sorted(queryset, key=lambda x: x.size_number, reverse=True)
        for obj in queryset:
            obj.seq = 1 + queryset.index(obj)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        top_killers = sorted(queryset, key=lambda x: x.statistic.kill, reverse=True)[:3]
        for obj in top_killers:
            obj.seq = 1 + top_killers.index(obj)
            

        top_hero_killers  = sorted(queryset, key=lambda x: x.statistic.hero_kill, reverse=True)[0:3]
        for obj in top_hero_killers:
            obj.hseq = 1 + top_hero_killers.index(obj)

        context["top_killers"] = top_killers
        context["top_hero_killer"] = top_hero_killers
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context