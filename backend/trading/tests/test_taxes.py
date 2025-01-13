from typing import override
from django.test import TestCase, override_settings
from django.conf import settings
from unittest.mock import patch
from profiles.models import User
from trading.models import Transaction, Tax, Account
from djmoney.money import Money


@override_settings(TAX_PERCENT=0.1)
class ExtractTaxTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.account = Account.objects.create(
            owner=self.user, balance=Money(1000, "USD")
        )

        self.tax_percent = settings.TAX_PERCENT

    def test_tax_extraction_on_transaction_creation(self):
        """Test that tax is correctly calculated and deducted when a transaction is created."""
        transaction = Transaction.objects.create(
            account=self.account, amount=Money(500, "USD"), t_type=Transaction.Type.BUY
        )

        # Verify the tax is calculated and created
        tax = Tax.objects.get(transaction=transaction)
        expected_tax = self.tax_percent * transaction.amount
        self.assertEqual(tax.amount, expected_tax)

        # Verify the account balance is reduced by the tax amount
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Money(1000, "USD") - expected_tax)

    def test_no_tax_extraction_on_transaction_update(self):
        """Test that tax is not recalculated or deducted when a transaction is updated."""
        transaction = Transaction.objects.create(
            account=self.account, amount=Money(500, "USD"), t_type=Transaction.Type.BUY
        )
        original_balance = self.account.balance

        # Update the transaction amount
        transaction.amount = Money(700, "USD")
        transaction.save()

        # Ensure no new tax entries are created
        taxes = Tax.objects.filter(transaction=transaction)
        self.assertEqual(taxes.count(), 1)

        # Ensure the account balance remains unchanged
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, original_balance)

    def test_multiple_transactions(self):
        """Test that multiple transactions are handled correctly, each with its own tax."""
        transaction1 = Transaction.objects.create(
            account=self.account, amount=Money(300, "USD"), t_type=Transaction.Type.BUY
        )
        transaction2 = Transaction.objects.create(
            account=self.account, amount=Money(200, "USD"), t_type=Transaction.Type.BUY
        )

        # Verify taxes are created for both transactions
        tax1 = Tax.objects.get(transaction=transaction1)
        tax2 = Tax.objects.get(transaction=transaction2)
        expected_tax1 = self.tax_percent * transaction1.amount
        expected_tax2 = self.tax_percent * transaction2.amount
        self.assertEqual(tax1.amount, expected_tax1)
        self.assertEqual(tax2.amount, expected_tax2)

        # Verify the account balance is reduced by the total tax
        self.account.refresh_from_db()
        self.assertEqual(
            self.account.balance, Money(1000, "USD") - (expected_tax1 + expected_tax2)
        )

    def test_zero_tax_on_zero_amount_transaction(self):
        """Test that no tax is deducted when the transaction amount is zero."""
        transaction = Transaction.objects.create(
            account=self.account, amount=Money(0, "USD"), t_type=Transaction.Type.BUY
        )

        # Verify no tax is created
        self.assertFalse(Tax.objects.filter(transaction=transaction).exists())

        # Verify the account balance remains unchanged
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Money(1000, "USD"))
