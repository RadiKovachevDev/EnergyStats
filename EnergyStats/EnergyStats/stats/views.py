from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MeasuringUnits, MarketType, DefaultCurrency
from django.shortcuts import render
from EnergyStats.common.statisctics_manager import StatisticsManager


@login_required
def statistics_view(request):
    weekly_data = StatisticsManager.fetch_weekly_data()
    weekly_average_price = StatisticsManager.average_price_by(weekly_data)
    weekly_total_volume = StatisticsManager.total_volume_by(weekly_data, MeasuringUnits.GWH)

    monthly_data = StatisticsManager.fetch_monthly_data()
    monthly_average_price = StatisticsManager.average_price_by(monthly_data)
    monthly_total_volume = StatisticsManager.total_volume_by(monthly_data, MeasuringUnits.GWH)

    yearly_data = StatisticsManager.fetch_yearly_data()
    yearly_average_price = StatisticsManager.average_price_by(yearly_data)
    yearly_total_volume = StatisticsManager.total_volume_by(yearly_data, MeasuringUnits.GWH)

    context = {
        'weekly': {
            'average_price': weekly_average_price,
            'total_volume': weekly_total_volume,
        },
        'monthly': {
            'average_price': monthly_average_price,
            'total_volume': monthly_total_volume,
        },
        'yearly': {
            'average_price': yearly_average_price,
            'total_volume': yearly_total_volume,
        },
    }

    return render(request, 'stats/stats.html', context)


def weekly_statistics_view(request):
    weekly_data = StatisticsManager.fetch_weekly_data()
    import json

    context = {
        'weekly': {
            'average_price': f"{StatisticsManager.average_price_by(weekly_data)} BGN",
            'total_volume': f"{StatisticsManager.total_volume_by(weekly_data, MeasuringUnits.GWH)} GWh",
            'min_price': f"{StatisticsManager.min_price_by(weekly_data)} BGN",
            'max_price': f"{StatisticsManager.max_price_by(weekly_data)} BGN",
            'min_volume': f"{StatisticsManager.min_volume_by(weekly_data)} GWh",
            'max_volume': f"{StatisticsManager.max_volume_by(weekly_data)} GWh",
            'dates': json.dumps([str(data.date) for data in weekly_data]),
            'prices': json.dumps([CalculationManager.get_average_price_by(data.date, MarketType.BASE, DefaultCurrency.BGN) for data in weekly_data]),
        }
    }

    return render(request, 'stats/weekly_stats.html', context)


def monthly_statistics_view(request):
    monthly_data = StatisticsManager.fetch_monthly_data()
    context = {
        'monthly': {
            'average_price': f"{StatisticsManager.average_price_by(monthly_data)} BGN",
            'total_volume': f"{StatisticsManager.total_volume_by(monthly_data, MeasuringUnits.GWH)} GWh",
            'min_price': f"{StatisticsManager.min_price_by(monthly_data)} BGN",
            'max_price': f"{StatisticsManager.max_price_by(monthly_data)} BGN",
            'min_volume': f"{StatisticsManager.min_volume_by(monthly_data)} GWh",
            'max_volume': f"{StatisticsManager.max_volume_by(monthly_data)} GWh",
            'dates': [str(data.date) for data in monthly_data],
            'prices': [CalculationManager.get_average_price_by(data.date, MarketType.BASE, DefaultCurrency.BGN) for data in monthly_data],
        }
    }
    return render(request, 'stats/monthly_stats.html', context)


def yearly_statistics_view(request):
    yearly_data = StatisticsManager.fetch_yearly_data()
    context = {
        'yearly': {
            'average_price': f"{StatisticsManager.average_price_by(yearly_data)} BGN",
            'total_volume': f"{StatisticsManager.total_volume_by(yearly_data, MeasuringUnits.GWH)} GWh",
            'min_price': f"{StatisticsManager.min_price_by(yearly_data)} BGN",
            'max_price': f"{StatisticsManager.max_price_by(yearly_data)} BGN",
            'min_volume': f"{StatisticsManager.min_volume_by(yearly_data)} GWh",
            'max_volume': f"{StatisticsManager.max_volume_by(yearly_data)} GWh",
            'dates': [str(data.date) for data in yearly_data],
            'prices': [CalculationManager.get_average_price_by(data.date, MarketType.BASE, DefaultCurrency.BGN) for data in yearly_data],
        }
    }
    return render(request, 'stats/yearly_stats.html', context)
