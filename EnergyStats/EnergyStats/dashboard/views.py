from datetime import date
from django.shortcuts import render

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MarketType, DefaultCurrency
from EnergyStats.common.local_data_manager import LocalDataManager


def dashboard_view(request):
    today = date.today()
    default_currency = DefaultCurrency.BGN
    energy_price = LocalDataManager.get_energy_price(today)
    peak_hours = LocalDataManager.get_hours_by(today, MarketType.PEAK)
    off_peak_hours = LocalDataManager.get_hours_by(today, MarketType.OFF_PEAK)
    hourly_info = LocalDataManager.get_hourly_info_for_current_hour(today)
    hourly_info_value = f"{round(CalculationManager.get_price_by(hourly_info, DefaultCurrency.BGN) / 1000, 5)} {default_currency}"
    min_price = f"{CalculationManager.get_min_price_by(today, MarketType.PEAK)} {default_currency}"
    max_price = f"{CalculationManager.get_max_price_by(today, MarketType.PEAK)} {default_currency}"
    min_volume = f"{CalculationManager.get_min_volume_by(today, MarketType.PEAK)} {default_currency}"
    max_volume = f"{CalculationManager.get_max_volume_by(today, MarketType.PEAK)} {default_currency}"
    current_volume = f"{hourly_info.volume} {default_currency}"
    total_volume = f"{CalculationManager.get_total_volume_for_day(today)} {default_currency}"
    average_price = f"{CalculationManager.get_average_price_by(today, MarketType.BASE, DefaultCurrency.BGN)} {default_currency}"
    average_price_peak = f"{CalculationManager.get_average_price_by(today, MarketType.PEAK, DefaultCurrency.BGN)} {default_currency}"
    average_price_off_peak = f"{CalculationManager.get_average_price_by(today, MarketType.OFF_PEAK, DefaultCurrency.BGN)} {default_currency}"

    context = {
        'peak_hours': peak_hours,
        'off_peak_hours': off_peak_hours,
        'today': today,
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
    return render(request, 'dashboard/dashboard.html', context)
