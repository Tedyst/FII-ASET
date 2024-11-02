import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Account)
def create_account_history(sender, instance, created, **kwargs):
    if not created:  # Only create history on updates, not on creation
        AccountHistory.objects.create(account=instance, amount=instance.balance)


# make sure account balance is not negative
@receiver(pre_save, sender=Account)
def check_account_balance(sender, instance, **kwargs):
    if instance.balance < 0:
        raise ValueError("Account balance cannot be negative.")


# log history of deposits/ withdrawals
@receiver(post_save, sender=AccountHistory)
def log_account_history_action(sender, instance, created, **kwargs):
    if created:
        action = "Deposit" if instance.amount > 0 else "Withdrawal"
        logger.debug(
            f"{action} of {instance.amount} recorded for account {instance.account.id}."
        )
