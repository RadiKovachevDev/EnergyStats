from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MarketType, DefaultCurrency
from EnergyStats.energy_service.models import EnergyPrice
from EnergyStats.common.local_data_manager import LocalDataManager


@login_required
def prices_view(request):
    prices = LocalDataManager.get_energy_prices()

    context = {
        'prices': prices
    }
    return render(request, 'prices/prices.html', context)


def price_details_view(request, date):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    price = get_object_or_404(EnergyPrice, date=selected_date)

    energy_price = LocalDataManager.get_energy_price(selected_date)
    peak_hours = LocalDataManager.get_hours_by(selected_date, MarketType.PEAK)
    off_peak_hours = LocalDataManager.get_hours_by(selected_date, MarketType.OFF_PEAK)
    hourly_info = LocalDataManager.get_hourly_info_for_current_hour(selected_date)
    hourly_info_value = f"{round(CalculationManager.get_price_by(hourly_info, DefaultCurrency.BGN) / 1000, 5)} {DefaultCurrency.BGN}"
    min_price = CalculationManager.get_min_price_by(selected_date, MarketType.PEAK)
    max_price = CalculationManager.get_max_price_by(selected_date, MarketType.PEAK)
    min_volume = CalculationManager.get_min_volume_by(selected_date, MarketType.PEAK)
    max_volume = CalculationManager.get_max_volume_by(selected_date, MarketType.PEAK)
    current_volume = f"{hourly_info.volume}" if hourly_info else "N/A"
    total_volume = CalculationManager.get_total_volume_for_day(selected_date)
    average_price = CalculationManager.get_average_price_by(selected_date, MarketType.BASE, DefaultCurrency.BGN)
    average_price_peak = CalculationManager.get_average_price_by(selected_date, MarketType.PEAK, DefaultCurrency.BGN)
    average_price_off_peak = CalculationManager.get_average_price_by(selected_date, MarketType.OFF_PEAK, DefaultCurrency.BGN)

    # Подготвяме контекста за шаблона
    context = {
        'price': price,
        'peak_hours': peak_hours,
        'off_peak_hours': off_peak_hours,
        'selected_date': selected_date,
        'hourly_info_value': hourly_info_value,
        'min_price': min_price,
        'max_price': max_price,
        'min_volume': min_volume,
        'max_volume': max_volume,
        'current_volume': current_volume,
        'total_volume': total_volume,
        'average_price': average_price,
        'average_price_peak': average_price_peak,
        'average_price_off_peak': average_price_off_peak,
    }

    return render(request, 'prices/price_details.html', context)