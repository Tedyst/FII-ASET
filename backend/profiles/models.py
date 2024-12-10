from typing import Iterable

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    identity_card_image = models.ImageField(
        upload_to="identity_cards/", blank=True, null=True
    )
    bank_statement_image = models.ImageField(
        upload_to="bank_statements/", blank=True, null=True
    )
    is_verified = models.BooleanField(default=False)
    iban = models.CharField(max_length=34, blank=True, null=True)
    personal_uid = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
