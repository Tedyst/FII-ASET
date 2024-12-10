import simple_history.admin
from django.contrib import admin

# Register your models here.
from .models import (
    Account,
    Exchange,
    ExternalMarketHolding,
    ExternalMarketOrder,
    MarketOrder,
    LimitOrder,
    StopOrder,
    Portfolio,
    Position,
    Security,
    Tax,
    Transaction,
)


class AccountAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("__str__", "owner", "balance")


class ExchangeAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("__str__", "url")


class OrderAdmin(simple_history.admin.SimpleHistoryAdmin):
    pass


class TransactionAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("__str__", "account", "amount", "date", "t_type", "created_at")


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Portfolio)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Security)
admin.site.register(Position)
admin.site.register(MarketOrder, OrderAdmin)
admin.site.register(LimitOrder, OrderAdmin)
admin.site.register(StopOrder, OrderAdmin)
admin.site.register(ExternalMarketHolding)
admin.site.register(ExternalMarketOrder)
admin.site.register(Tax)
