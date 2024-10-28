from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Position)
def set_bought_at(sender, instance, created, **kwargs):
    if created and instance.bought_at is None:
        current_price = instance.ticker.price
        instance.bought_at = current_price
        instance.save()

# create record for price change in ticker history
@receiver(post_save, sender=Ticker)
def create_ticker_history(sender, instance, created, **kwargs):
    if not created:  
        TickerHistory.objects.create(ticker=instance, price=instance.price)

# check if Positon was sold and set ended_at
@receiver(post_save, sender=Position)
def set_ended_at_on_sell(sender, instance, created, **kwargs):
    if created:
        return
    
    if not instance.ended_at:
        instance.ended_at = timezone.now()  
        instance.save(update_fields=['ended_at'])  # save only the changed field