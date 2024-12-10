from datetime import date, datetime
from django.shortcuts import render

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MarketType, DefaultCurrency
from EnergyStats.common.local_data_manager import LocalDataManager
from EnergyStats.energy_service.cron import UpdatePricesCronJob


def dashboard_view(request):

    today = date.today()
    energy_price = LocalDataManager.get_energy_price(today).first()

    dates = []
    prices = []

    if energy_price:
        for hourly_data in energy_price.hourly_data.all():
            time_obj = datetime.strptime(hourly_data.time, "%H:%M:%S")
            dates.append(time_obj.strftime("%H:%M"))
            price = CalculationManager.get_price_by(hourly_data.data, DefaultCurrency.BGN)
            prices.append(price)

    current_time = datetime.now().strftime("%H:00:00")
    default_currency = DefaultCurrency.BGN

    peak_hours = LocalDataManager.get_hours_by(today, MarketType.PEAK)
    off_peak_hours = LocalDataManager.get_hours_by(today, MarketType.OFF_PEAK)
    hourly_info = LocalDataManager.get_hourly_info_for_current_hour(today)

    context = {
        'current_time': current_time,
        'peak_hours': peak_hours,
        'off_peak_hours': off_peak_hours,
        'dates': dates,
        'prices': prices,
        'hourly_info_value': f"{round(CalculationManager.get_price_by(hourly_info, default_currency) / 1000, 5)} {default_currency}",
        'min_price': f"{CalculationManager.get_min_price_by(today, MarketType.PEAK)} {default_currency}",
        'max_price': f"{CalculationManager.get_max_price_by(today, MarketType.PEAK)} {default_currency}",
        'min_volume': f"{CalculationManager.get_min_volume_by(today, MarketType.PEAK)} {default_currency}",
        'max_volume': f"{CalculationManager.get_max_volume_by(today, MarketType.PEAK)} {default_currency}",
        'current_volume': f"{hourly_info.volume} {default_currency}" if hourly_info else "N/A",
        'total_volume': f"{CalculationManager.get_total_volume_for_day(today)} {default_currency}",
        'average_price': f"{CalculationManager.get_average_price_by(today, MarketType.BASE, default_currency)} {default_currency}",
        'average_price_peak': f"{CalculationManager.get_average_price_by(today, MarketType.PEAK, default_currency)} {default_currency}",
        'average_price_off_peak': f"{CalculationManager.get_average_price_by(today, MarketType.OFF_PEAK, default_currency)} {default_currency}",
    }

    return render(request, 'dashboard/dashboard.html', context)
