import decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money
from trading.models import Account
from unittest.mock import patch
from allauth.account.signals import (
    email_changed,
    email_confirmed,
    email_confirmation_sent,
)
from .models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="password1234")

        # check if user was created correctly
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password1234"))

        # ensure this user is not a superuser
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpass12#"
        )

        # check if admin user was created correctly
        self.assertIsInstance(admin_user, User)
        self.assertEqual(admin_user.username, "adminuser")
        self.assertTrue(admin_user.check_password("adminpass12#"))

        # check if superuser has correct role
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


class AccountModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="Parola44")

    def test_create_account(self):
        # create and check if account was created correctly
        account = Account.objects.create(
            owner=self.user, balance=Money("100.00", currency="USD")
        )
        self.assertIsInstance(account, Account)
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.balance, Money("100.00", currency="USD"))

    def test_account_balance_precision(self):
        # check if balance respects max_digits and decimal_places
        account = Account.objects.create(
            owner=self.user, balance=Money("123456.78", currency="USD")
        )
        self.assertEqual(account.balance, Money("123456.78", currency="USD"))

        with self.assertRaises(decimal.InvalidOperation):
            Account.objects.create(
                owner=self.user, balance=Money("12345678901234567.89", currency="USD")
            )  # More than max_digits

    def test_account_auto_fields(self):
        # ensure created_at and updated_at fields are set automatically
        account = Account.objects.create(
            owner=self.user, balance=Money("50.00", currency="USD")
        )
        self.assertIsNotNone(account.created_at)
        self.assertIsNotNone(account.updated_at)


class SignalTests(TestCase):

    @patch("profiles.signals.logger")
    def test_email_confirmation_sent_signal(self, mock_logger):
        email_address = "test@example.com"
        confirmation = type(
            "Confirmation",
            (object,),
            {
                "email_address": type(
                    "EmailAddress", (object,), {"email": email_address}
                )
            },
        )
        email_confirmation_sent.send(
            sender=None, request=None, confirmation=confirmation, signup=False
        )
        mock_logger.info.assert_called_with(
            f"Email confirmation sent to: {email_address}"
        )

    @patch("profiles.signals.logger")
    def test_email_confirmed_signal(self, mock_logger):
        email_address = type("EmailAddress", (object,), {"email": "test@example.com"})
        email_confirmed.send(sender=None, request=None, email_address=email_address)
        mock_logger.info.assert_called_with(
            f"Email confirmed for: {email_address.email}"
        )

    @patch("profiles.signals.logger")
    def test_email_changed_signal(self, mock_logger):
        user = User.objects.create(username="testuser")
        from_email_address = type(
            "EmailAddress", (object,), {"email": "old@example.com"}
        )
        to_email_address = type("EmailAddress", (object,), {"email": "new@example.com"})
        email_changed.send(
            sender=None,
            request=None,
            user=user,
            from_email_address=from_email_address,
            to_email_address=to_email_address,
        )
        mock_logger.info.assert_called_with(
            f"Email changed for user: {user.username} from {from_email_address.email} to {to_email_address.email}"
        )
