import logging

from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from djmoney.money import Money

from .models import Exchange, Security, Position, Order, Tax, Transaction
from .tasks import update_security_price

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Exchange)
def set_default_exchange_name(sender, instance, *args, **kwargs):
    if not instance.short_name:
        instance.short_name = instance.name[:3].upper()


@receiver(post_save)
def log_saved_models(sender, instance, created=False, *args, **kwargs):
    logger.info(f"Saved model of type {sender}, {instance=}, {created=}")


@receiver(post_save, sender=Security)
def update_security_price_on_create(sender, instance, created=False, *args, **kwargs):
    if created and not settings.TESTING:
        logger.info(f"Updating price for {instance.symbol}")
        update_security_price.delay(instance.pk)


@receiver(post_save, sender=Position)
@receiver(post_delete, sender=Position)
def update_users_purchased(sender, instance, **kwargs):
    """
    Updates the `users_purchased` field on the Security model whenever a
    Position is created, updated, or deleted.
    """
    security = instance.security
    # Count the number of distinct portfolios holding this security
    portfolios_count = (
        Position.objects.filter(security=security)
        .values("portfolio")
        .distinct()
        .count()
    )
    security.users_purchased = portfolios_count
    security.save()


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if "status" in instance.get_dirty_fields():
        logger.info(f"Order status changed: {instance} to {instance.status}")


@receiver(post_save, sender=Transaction)
@transaction.atomic
def extract_tax(sender, instance, created=False, **kwargs):
    if created and instance.amount > Money(0, instance.amount.currency):
        logger.info(f"Extracting tax for {instance}")
        tax = settings.TAX_PERCENT * instance.amount
        Tax.objects.create(amount=tax, transaction=instance)
        instance.account.balance -= tax
        instance.account.save()
