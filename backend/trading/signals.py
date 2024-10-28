from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Position


@receiver(post_save, sender=Position)
def set_bought_at(sender, instance, created, **kwargs):
    if created and instance.bought_at is None:
        current_price = instance.ticker.price
        instance.bought_at = current_price
        instance.save()