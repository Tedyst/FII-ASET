import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Exchange, Security
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
