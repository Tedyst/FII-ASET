import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver
from .models import User
from allauth.account.signals import (
    email_changed,
    email_confirmed,
    email_confirmation_sent,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user created: {instance.username}")
    else:
        logger.info(f"User updated: {instance.username}")


@receiver(email_confirmation_sent)
def email_confirmation_sent_handler(request, confirmation, signup, **kwargs):
    logger.info(f"Email confirmation sent to: {confirmation.email_address.email}")


@receiver(email_confirmed)
def email_confirmed_handler(request, email_address, **kwargs):
    logger.info(f"Email confirmed for: {email_address.email}")


@receiver(email_changed)
def email_changed_handler(
    request, user, from_email_address, to_email_address, **kwargs
):
    logger.info(
        f"Email changed for user: {user.username} from {from_email_address.email} to {to_email_address.email}"
    )


documents_submitted = Signal()
documents_approved = Signal()
documents_rejected = Signal()


@receiver(documents_submitted)
def handle_documents_submitted(sender, user, **kwargs):
    logger.info(f"Documents submitted for verification by user: {user.username}")


@receiver(documents_approved)
def handle_documents_approved(sender, user, **kwargs):
    logger.info(f"Documents approved for user: {user.username}")


@receiver(documents_rejected)
def handle_documents_rejected(sender, user, **kwargs):
    logger.info(f"Documents rejected for user: {user.username}")
