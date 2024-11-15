import logging

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Exchange, Security, Position
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
    if created:
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
