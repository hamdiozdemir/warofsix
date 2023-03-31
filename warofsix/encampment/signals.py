from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import DepartingCampaigns, DepartingTroops, ArrivingCampaigns, ArrivingTroops
from main.models import UserTroops, UserTracker
from django.utils import timezone
from main.views import positive_or_zero
import time



