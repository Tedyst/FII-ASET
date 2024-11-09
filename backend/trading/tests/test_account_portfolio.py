from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from djmoney.money import Money
from profiles.models import User
from trading.models import (
    Account,
    Exchange,
    Order,
    Portfolio,
    Position,
    Security,
    Transaction,
)


class AccountPortfolioTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.account = Account.objects.create(
            owner=self.user, balance=Money(10000, "USD")
        )
        self.portfolio = Portfolio.objects.create(account=self.account)
        self.exchange = Exchange.objects.create(name="NYSE", url="http://nyse.com")
        self.security = Security.objects.create(
            name="Apple Inc.",
            symbol="AAPL",
            price=Money(150, "USD"),
            exchange=self.exchange,
        )

    def test_portfolio_value_initially_zero(self):
        """Portfolio value should be zero initially (no positions)."""
        self.assertEqual(self.portfolio.value(), 0)

    def test_order_fill_buy_creates_position_and_transaction(self):
        """Test a buy order creates a position and updates balance correctly."""
        order = Order.objects.create(
            account=self.account,
            security=self.security,
            quantity=Decimal("10"),
            price=Money(150, "USD"),
            t_type=Order.Type.BUY,
            status=Order.Status.PENDING,
            order_type=Order.OrderType.MARKET,
        )

        order.fill()
        # Check balance deduction
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Money(8500, "USD"))

        # Check position created
        position = self.portfolio.positions.get(security=self.security)
        self.assertEqual(position.quantity, Decimal("10"))
        self.assertEqual(position.average_price, Money(150, "USD"))

        # Check transaction recorded
        transaction = Transaction.objects.get(
            account=self.account, t_type=Transaction.Type.BUY
        )
        self.assertEqual(transaction.amount, Money(1500, "USD"))

    def test_order_fill_sell_updates_position_and_transaction(self):
        """Test a sell order updates a position and adds funds to account."""
        # Create initial position
        Position.objects.create(
            portfolio=self.portfolio,
            security=self.security,
            quantity=Decimal("10"),
            average_price=Money(150, "USD"),
        )

        order = Order.objects.create(
            account=self.account,
            security=self.security,
            quantity=Decimal("5"),
            price=Money(160, "USD"),
            t_type=Order.Type.SELL,
            status=Order.Status.PENDING,
            order_type=Order.OrderType.MARKET,
        )

        order.fill()
        # Check balance increase
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Money(10800, "USD"))

        # Check position updated
        position = self.portfolio.positions.get(security=self.security)
        self.assertEqual(position.quantity, Decimal("5"))

        # Check transaction recorded
        transaction = Transaction.objects.get(
            account=self.account, t_type=Transaction.Type.SELL
        )
        self.assertEqual(transaction.amount, Money(800, "USD"))

    def test_order_cancellation(self):
        """Test that cancelling an order only updates its status."""
        order = Order.objects.create(
            account=self.account,
            security=self.security,
            quantity=Decimal("10"),
            price=Money(150, "USD"),
            t_type=Order.Type.BUY,
            status=Order.Status.PENDING,
            order_type=Order.OrderType.MARKET,
        )

        order.cancel()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CANCELLED)

        # Account balance and portfolio should remain unchanged
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Money(10000, "USD"))
        self.assertEqual(self.portfolio.value(), 0)

    def test_position_value_and_profit(self):
        """Test position value and profit calculation."""
        position = Position.objects.create(
            portfolio=self.portfolio,
            security=self.security,
            quantity=Decimal("10"),
            average_price=Money(120, "USD"),
        )
        self.security.price = Money(150, "USD")
        self.security.save()

        # Check position value and profit
        self.assertEqual(position.value(), Money(1200, "USD"))
        self.assertEqual(position.profit(), Money(300, "USD"))

    def test_portfolio_value_calculation(self):
        """Test portfolio value reflects total of all positions."""
        Position.objects.create(
            portfolio=self.portfolio,
            security=self.security,
            quantity=Decimal("10"),
            average_price=Money(150, "USD"),
        )
        another_security = Security.objects.create(
            name="Google LLC",
            symbol="GOOGL",
            price=Money(2800, "USD"),
            exchange=self.exchange,
        )
        Position.objects.create(
            portfolio=self.portfolio,
            security=another_security,
            quantity=Decimal("5"),
            average_price=Money(2700, "USD"),
        )

        # Portfolio value should reflect both positions
        self.assertEqual(
            self.portfolio.value(), Money(1500, "USD") + Money(13500, "USD")
        )
