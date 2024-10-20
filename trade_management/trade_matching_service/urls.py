from django.urls import path
from . import views

urlpatterns = [
    path('trades/', views.fetch_all_trades, name='fetch_all_trades'),
    # You can add more URL patterns as needed
]
