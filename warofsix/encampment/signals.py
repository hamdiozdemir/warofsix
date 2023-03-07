from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import DepartingCampaigns, DepartingTroops, ArrivingCampaigns, ArrivingTroops
from main.models import UserTroops, UserTracker
from django.utils import timezone
from main.views import positive_or_zero


# @receiver(post_save, sender=UserTracker)
# def catch_campaigns(sender, instance, **kwargs):
#     departing_time_check(instance.user)
#     print("****** Departing Çalıştı********")




# def departing_time_check(user):
#     campaigns = DepartingCampaigns.objects.filter(user=user)
#     for camp in campaigns:
#         time_diff = (timezone.now() - camp.last_checkout).total_seconds()
#         if positive_or_zero(time_diff) == 0:
#             camp.time_left = 0
#             camp.last_checkout = timezone.now()
#             camp.save()
#         else:
#             camp.time_left -= time_diff
#             camp.last_checkout = timezone.now()
#             camp.save()
#     return True