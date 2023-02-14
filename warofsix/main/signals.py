from django.dispatch import receiver
from django.db.models.signals import post_save
# from .models import UserTroops, Race

# @receiver(post_save, sender=Race)
# def create_instances(sender, instance, created, **kwargs):
#     if created:
#         UserTroops.objects.create(user=instance, troop = instance.name)
