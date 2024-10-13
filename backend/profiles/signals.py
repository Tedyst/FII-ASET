from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, AccountHistory


@receiver(post_save, sender=Account)
def create_account_history(sender, instance, created, **kwargs):
    if not created:  # Only create history on updates, not on creation
        AccountHistory.objects.create(
            account=instance,
            amount=instance.balance
        )