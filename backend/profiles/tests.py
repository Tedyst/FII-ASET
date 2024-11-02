import decimal
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import *


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
        account = Account.objects.create(owner=self.user, balance=Decimal("100.00"))
        self.assertIsInstance(account, Account)
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.balance, Decimal("100.00"))

    def test_account_balance_precision(self):
        # check if balance respects max_digits and decimal_places
        account = Account.objects.create(owner=self.user, balance=Decimal("123456.78"))
        self.assertEqual(account.balance, Decimal("123456.78"))

        with self.assertRaises(decimal.InvalidOperation):
            Account.objects.create(
                owner=self.user, balance=Decimal("12345678901.89")
            )  # More than max_digits

    def test_account_auto_fields(self):
        # ensure created_at and updated_at fields are set automatically
        account = Account.objects.create(owner=self.user, balance=Decimal("50.00"))
        self.assertIsNotNone(account.created_at)
        self.assertIsNotNone(account.updated_at)


class AccountHistoryModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="password123!"
        )
        self.account = Account.objects.create(
            owner=self.user, balance=Decimal("500.00")
        )

    def test_create_account_history(self):
        # create an account history entry and verify its properties
        history = AccountHistory.objects.create(
            account=self.account, amount=Decimal("100.00")
        )
        self.assertIsInstance(history, AccountHistory)
        self.assertEqual(history.account, self.account)
        self.assertEqual(history.amount, Decimal("100.00"))

    def test_account_history_auto_created_at(self):
        # ensure created_at field is set automatically
        history = AccountHistory.objects.create(
            account=self.account, amount=Decimal("200.00")
        )
        self.assertIsNotNone(history.created_at)

    def test_account_history_negative_amount(self):
        # check if the account history can handle both deposits and withdrawals
        deposit = AccountHistory.objects.create(
            account=self.account, amount=Decimal("150.00")
        )
        withdrawal = AccountHistory.objects.create(
            account=self.account, amount=Decimal("-50.00")
        )
        self.assertEqual(deposit.amount, Decimal("150.00"))
        self.assertEqual(withdrawal.amount, Decimal("-50.00"))
