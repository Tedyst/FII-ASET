import simple_history.admin
from django.contrib import admin

# Register your models here.
from .models import Account, Exchange, Order, Portfolio, Position, Security, Transaction


class AccountAdmin(simple_history.admin.SimpleHistoryAdmin):
    pass


class OrderAdmin(simple_history.admin.SimpleHistoryAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)
admin.site.register(Portfolio)
admin.site.register(Exchange)
admin.site.register(Security)
admin.site.register(Position)
admin.site.register(Order, OrderAdmin)
