# your_app_name/urls.py
from django.urls import path
from .views import (
    place_order,
    modify_order,
    cancel_order,
    fetch_order,
    fetch_all_orders,
    fetch_all_trades,
    fetch_trade,
)

urlpatterns = [
    path('orders/place/', place_order, name='place_order'),                      # POST: Place an order
    path('orders/modify/', modify_order, name='modify_order'),     # PUT: Modify an order
    path('orders/<int:order_id>/cancel/', cancel_order, name='cancel_order'),  # DELETE: Cancel an order
    path('orders/<int:order_id>/', fetch_order, name='fetch_order'),       # GET: Fetch order details
    path('orders/', fetch_all_orders, name='fetch_all_orders'),             # GET: Fetch all orders
    path('trades/', fetch_all_trades, name='fetch_all_trades'),             # GET: Fetch all trades
    path('trades/<int:trade_id>/', fetch_trade, name='fetch_trade'),        # GET: Fetch a single trade
]
