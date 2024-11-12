import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Exchange

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Exchange)
def set_default_exchange_name(sender, instance, *args, **kwargs):
    if not instance.short_name:
        instance.short_name = instance.name[:3].upper()


@receiver(post_save)
def log_saved_models(sender, instance, created=False, *args, **kwargs):
    logger.info(f"Saved model of type {sender}, {instance=}, {created=}")
