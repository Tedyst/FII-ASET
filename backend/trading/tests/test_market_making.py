from django.test import TestCase
from unittest.mock import patch
from profiles.models import User
from trading.models import Exchange, MarketOrder, Order, Portfolio, Security, Account
from trading.tasks import market_making_market_orders
from djmoney.money import Money


class MarketMakingMarketOrdersTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test", password="test")
        self.user2 = User.objects.create_user(username="test2", password="test2")
        self.exchange = Exchange.objects.create(name="Test Exchange")
        # Create test data: accounts and securities
        self.account1 = Account.objects.create(owner=self.user1)
        self.account2 = Account.objects.create(owner=self.user2)
        self.portfolio1 = Portfolio.objects.create(account=self.account1)
        self.portfolio2 = Portfolio.objects.create(account=self.account2)
        self.security = Security.objects.create(
            name="Security A",
            symbol="SEC",
            price=Money(100, "USD"),
            exchange=self.exchange,
        )

    def test_full_match(self):
        """Test that buy and sell market orders with equal quantities are fully matched."""
        sell_order = MarketOrder.objects.create(
            account=self.account1,
            security=self.security,
            t_type=Order.Type.SELL,
            quantity=10,
            status=Order.Status.PENDING,
        )
        buy_order = MarketOrder.objects.create(
            account=self.account2,
            security=self.security,
            t_type=Order.Type.BUY,
            quantity=10,
            status=Order.Status.PENDING,
        )

        market_making_market_orders()

        sell_order.refresh_from_db()
        buy_order.refresh_from_db()

        self.assertEqual(sell_order.status, Order.Status.FILLED)
        self.assertEqual(buy_order.status, Order.Status.FILLED)

    def test_partial_match_sell_larger(self):
        """Test that a sell order larger than a buy order leaves a new sell market order."""
        sell_order = MarketOrder.objects.create(
            account=self.account1,
            security=self.security,
            t_type=Order.Type.SELL,
            quantity=15,
            status=Order.Status.PENDING,
        )
        buy_order = MarketOrder.objects.create(
            account=self.account2,
            security=self.security,
            t_type=Order.Type.BUY,
            quantity=10,
            status=Order.Status.PENDING,
        )

        market_making_market_orders()

        sell_order.refresh_from_db()
        buy_order.refresh_from_db()
        new_order = MarketOrder.objects.get(status=Order.Status.PENDING)

        self.assertEqual(sell_order.status, Order.Status.FILLED)
        self.assertEqual(buy_order.status, Order.Status.FILLED)
        self.assertEqual(new_order.quantity, 5)
        self.assertEqual(new_order.t_type, Order.Type.SELL)

    def test_partial_match_buy_larger(self):
        """Test that a buy order larger than a sell order leaves a new buy market order."""
        sell_order = MarketOrder.objects.create(
            account=self.account1,
            security=self.security,
            t_type=Order.Type.SELL,
            quantity=10,
            status=Order.Status.PENDING,
        )
        buy_order = MarketOrder.objects.create(
            account=self.account2,
            security=self.security,
            t_type=Order.Type.BUY,
            quantity=15,
            status=Order.Status.PENDING,
        )

        market_making_market_orders()

        sell_order.refresh_from_db()
        buy_order.refresh_from_db()
        new_order = MarketOrder.objects.get(status=Order.Status.PENDING)

        self.assertEqual(sell_order.status, Order.Status.FILLED)
        self.assertEqual(buy_order.status, Order.Status.FILLED)
        self.assertEqual(new_order.quantity, 5)
        self.assertEqual(new_order.t_type, Order.Type.BUY)

    @patch("trading.tasks.ExternalMarketOrder.objects.create")
    def test_not_matched_orders_create_external(self, mock_create):
        """Test that unmatched orders are passed to ExternalMarketOrder."""
        MarketOrder.objects.create(
            account=self.account1,
            security=self.security,
            t_type=Order.Type.SELL,
            quantity=10,
            status=Order.Status.PENDING,
        )
        MarketOrder.objects.create(
            account=self.account2,
            security=self.security,
            t_type=Order.Type.BUY,
            quantity=5,
            status=Order.Status.PENDING,
        )

        market_making_market_orders()

        # Verify unmatched orders are passed to ExternalMarketOrder
        unmatched_orders = MarketOrder.objects.filter(status=Order.Status.PENDING)
        self.assertEqual(unmatched_orders.count(), 1)
        mock_create.assert_called_once_with(order=unmatched_orders.first())

    def test_no_pending_orders(self):
        """Test that the function does nothing when there are no pending orders."""
        MarketOrder.objects.create(
            account=self.account1,
            security=self.security,
            t_type=Order.Type.SELL,
            quantity=10,
            status=Order.Status.FILLED,
        )
        MarketOrder.objects.create(
            account=self.account2,
            security=self.security,
            t_type=Order.Type.BUY,
            quantity=10,
            status=Order.Status.FILLED,
        )

        with patch("trading.tasks.logger.info") as mock_logger:
            market_making_market_orders()
            mock_logger.assert_not_called()

    def test_multiple_securities(self):
        """Test that orders for different securities are processed independently."""
        security_b = Security.objects.create(
            name="Security B",
            symbol="SEC_B",
            price=Money(100, "USD"),
            exchange=self.exchange,
        )
        MarketOrder.objects.create(
            account=self.account1,
            security=self.security,
            t_type=Order.Type.SELL,
            quantity=10,
            status=Order.Status.PENDING,
        )
        MarketOrder.objects.create(
            account=self.account2,
            security=self.security,
            t_type=Order.Type.BUY,
            quantity=10,
            status=Order.Status.PENDING,
        )
        MarketOrder.objects.create(
            account=self.account1,
            security=security_b,
            t_type=Order.Type.SELL,
            quantity=5,
            status=Order.Status.PENDING,
        )
        MarketOrder.objects.create(
            account=self.account2,
            security=security_b,
            t_type=Order.Type.BUY,
            quantity=5,
            status=Order.Status.PENDING,
        )

        market_making_market_orders()

        # Verify all orders are matched
        self.assertFalse(
            MarketOrder.objects.filter(status=Order.Status.PENDING).exists()
        )
