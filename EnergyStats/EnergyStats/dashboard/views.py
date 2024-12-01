from datetime import date
from django.shortcuts import render

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MarketType, DefaultCurrency
from EnergyStats.common.local_data_manager import LocalDataManager


def dashboard_view(request):
    today = date.today()
    energy_price = LocalDataManager.get_energy_price(today)
    peak_hours = LocalDataManager.get_hours_by(today, MarketType.PEAK)
    off_peak_hours = LocalDataManager.get_hours_by(today, MarketType.PEAK)
    hourly_info = LocalDataManager.get_hourly_info_for_current_hour(today)
    hourly_info_value = f"{round(CalculationManager.get_price_by(hourly_info, DefaultCurrency.BGN) / 1000, 5)} {DefaultCurrency.BGN}"
    min_price = CalculationManager.get_min_price_by(today, MarketType.PEAK)
    max_price = CalculationManager.get_max_price_by(today, MarketType.PEAK)
    min_volume = CalculationManager.get_min_volume_by(today, MarketType.PEAK)
    max_volume = CalculationManager.get_max_volume_by(today, MarketType.PEAK)
    current_volume = f"{hourly_info.volume}"
    total_volume = CalculationManager.get_total_volume_for_day(today)
    average_price = CalculationManager.get_average_price_by(today, MarketType.BASE, DefaultCurrency.BGN)
    average_price_peak = CalculationManager.get_average_price_by(today, MarketType.PEAK, DefaultCurrency.BGN)
    average_price_off_peak = CalculationManager.get_average_price_by(today, MarketType.OFF_PEAK, DefaultCurrency.BGN)

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
