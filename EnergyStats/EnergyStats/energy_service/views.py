from django.http import JsonResponse
from .services import fetch_prices, fetch_latest_price, fetch_latest_price_date


def update_prices(request):
    fetch_prices()
    return JsonResponse({"status": "Prices updated successfully"})


def update_latest_price(request):
    fetch_latest_price()
    return JsonResponse({"status": "Latest price updated successfully"})


def update_latest_price_date(request):
    fetch_latest_price_date()
    return JsonResponse({"status": "Latest price date updated successfully"})
