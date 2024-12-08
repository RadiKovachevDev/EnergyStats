from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import DefaultCurrency
from EnergyStats.common.local_data_manager import LocalDataManager
from EnergyStats.common.statisctics_manager import StatisticsManager
from EnergyStats.stats.models import EnergyStatistic


@login_required
def statistics_view(request):
    weekly_data = StatisticsManager.fetch_weekly_data()
    weekly_average_price = StatisticsManager.average_price_by(weekly_data)
    weekly_total_volume = StatisticsManager.total_volume_by(weekly_data, measuring_units='gWh')
    weekly_min_price = StatisticsManager.min_price_by(weekly_data)
    weekly_max_price = StatisticsManager.max_price_by(weekly_data)
    weekly_min_volume = StatisticsManager.min_volume_by(weekly_data)
    weekly_max_volume = StatisticsManager.max_volume_by(weekly_data)

    monthly_data = StatisticsManager.fetch_monthly_data()
    monthly_average_price = StatisticsManager.average_price_by(monthly_data)
    monthly_total_volume = StatisticsManager.total_volume_by(monthly_data, measuring_units='gWh')
    monthly_min_price = StatisticsManager.min_price_by(monthly_data)
    monthly_max_price = StatisticsManager.max_price_by(monthly_data)
    monthly_min_volume = StatisticsManager.min_volume_by(monthly_data)
    monthly_max_volume = StatisticsManager.max_volume_by(monthly_data)

    yearly_data = StatisticsManager.fetch_yearly_data()
    yearly_average_price = StatisticsManager.average_price_by(yearly_data)
    yearly_total_volume = StatisticsManager.total_volume_by(yearly_data, measuring_units='gWh')
    yearly_min_price = StatisticsManager.min_price_by(yearly_data)
    yearly_max_price = StatisticsManager.max_price_by(yearly_data)
    yearly_min_volume = StatisticsManager.min_volume_by(yearly_data)
    yearly_max_volume = StatisticsManager.max_volume_by(yearly_data)

    context = {
        'weekly': {
            'average_price': weekly_average_price,
            'total_volume': weekly_total_volume,
            'min_price': weekly_min_price,
            'max_price': weekly_max_price,
            'min_volume': weekly_min_volume,
            'max_volume': weekly_max_volume,
        },
        'monthly': {
            'average_price': monthly_average_price,
            'total_volume': monthly_total_volume,
            'min_price': monthly_min_price,
            'max_price': monthly_max_price,
            'min_volume': monthly_min_volume,
            'max_volume': monthly_max_volume,
        },
        'yearly': {
            'average_price': yearly_average_price,
            'total_volume': yearly_total_volume,
            'min_price': yearly_min_price,
            'max_price': yearly_max_price,
            'min_volume': yearly_min_volume,
            'max_volume': yearly_max_volume,
        },
    }

    return render(request, 'stats/stats.html', context)

