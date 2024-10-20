from django.contrib import admin
from .models import Order, Trade

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'side', 'price', 'quantity', 'remaining_quantity', 'average_traded_price', 'status', 'created_at')
    list_filter = ('side', 'status', 'created_at')
    search_fields = ('id', 'side', 'status')
    ordering = ('-created_at',)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid_order_id', 'ask_order_id', 'traded_quantity', 'execution_price', 'execution_timestamp')
    list_filter = ('execution_timestamp',)
    search_fields = ('bid_order_id', 'ask_order_id')
    ordering = ('-execution_timestamp',)
