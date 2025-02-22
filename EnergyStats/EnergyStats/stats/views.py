import time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MeasuringUnits, MarketType, DefaultCurrency
from django.shortcuts import render

from EnergyStats.common.local_data_manager import LocalDataManager
from EnergyStats.common.statisctics_manager import StatisticsManager


@login_required
def statistics_view(request):
    yearly_data = list(LocalDataManager.get_yearly_energy_prices())
    context = StatisticsManager.calculate_price_volume_statistics(yearly_data)
    return render(request, 'stats/stats.html', context)


def weekly_statistics_view(request):
    weekly_data = list(LocalDataManager.get_weekly_energy_prices())
    context = StatisticsManager.calculate_statistics(weekly_data,"weekly")

    return render(request, 'stats/weekly_stats.html', context)


def monthly_statistics_view(request):
    monthly_data = list(LocalDataManager.get_monthly_energy_prices())
    context = StatisticsManager.calculate_statistics(monthly_data,"monthly")

    return render(request, 'stats/monthly_stats.html', context)


def yearly_statistics_view(request):
    yearly_data = list(LocalDataManager.get_yearly_energy_prices())
    context = StatisticsManager.calculate_statistics(yearly_data,"yearly")

    return render(request, 'stats/yearly_stats.html', context)
