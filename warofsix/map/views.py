from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Location, Notifications

# Create your views here.


class MapView(LoginRequiredMixin, TemplateView):
    template_name = "map/map.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        locations = Location.objects.all().order_by('-locy', 'locx')
        context["locations"] = locations

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notify = Notifications.objects.get(user = self.request.user)
        context["notify"] = notify
        return context







