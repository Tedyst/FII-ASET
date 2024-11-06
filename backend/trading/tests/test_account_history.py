from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money
from trading.models import Account

User = get_user_model()


class AccountHistoryTest(TestCase):
    def setUp(self):
        # Create a user to associate with the account
        self.user = User.objects.create(username="testuser", password="password")

    def test_account_history(self):
        # Step 1: Create an Account and check initial history
        account = Account.objects.create(owner=self.user, balance=Money(100, "USD"))
        self.assertEqual(
            account.history.count(), 1
        )  # Should have one entry in history (creation)

        initial_history = account.history.first()
        self.assertEqual(initial_history.balance, Money(100, "USD"))

        # Step 2: Update the Account balance
        account.balance = Money(200, "USD")
        account.save()

        # Step 3: Check that the history now has two entries
        self.assertEqual(account.history.count(), 2)

        # Fetch the latest history record and confirm it reflects the change
        latest_history = account.history.first()
        self.assertEqual(latest_history.balance, Money(200, "USD"))

        # Check that the previous history entry still has the old balance
        previous_history = account.history.last()
        self.assertEqual(previous_history.balance, Money(100, "USD"))
