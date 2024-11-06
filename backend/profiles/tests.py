import decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money
from trading.models import Account

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
