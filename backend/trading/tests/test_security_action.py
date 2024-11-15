from django.test import TestCase
from ..models import Portfolio, Position, Security


class SecurityUsersPurchasedSignalTest(TestCase):
    def test_users_purchased_updates_on_position_change(self):
        # Setup
        security = Security.objects.create(
            name="Test Stock", symbol="TEST", price="100.00"
        )
        portfolio1 = Portfolio.objects.create(name="Portfolio 1")
        portfolio2 = Portfolio.objects.create(name="Portfolio 2")

        # Add positions
        Position.objects.create(
            portfolio=portfolio1, quantity=10, average_price="100.00", security=security
        )
        self.assertEqual(security.users_purchased, 1)

        Position.objects.create(
            portfolio=portfolio2, quantity=5, average_price="100.00", security=security
        )
        security.refresh_from_db()
        self.assertEqual(security.users_purchased, 2)

        # Delete a position
        Position.objects.filter(portfolio=portfolio1).delete()
        security.refresh_from_db()
        self.assertEqual(security.users_purchased, 1)
