from django.urls import path
from .views import update_prices, update_latest_price, update_latest_price_date

urlpatterns = [
    path('update-prices/', update_prices, name='update_prices'),
    path('update-latest-price/', update_latest_price, name='update_latest_price'),
    path('update-latest-price-date/', update_latest_price_date, name='update_latest_price_date'),
]
