from datetime import datetime
import calendar
from typing import final
from django.utils.timezone import now
from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MarketType, DefaultCurrency, MeasuringUnits


@final
class StatisticsManager:
    current_date = datetime.now()
    calendar = calendar.Calendar()
    date_formatter = "%d.%m.%Y"

    @staticmethod
    def calculate_price_volume_statistics(energy_prices):
        current_date = now()
        current_week = current_date.isocalendar().week
        current_month = current_date.month
        current_year = current_date.year

        weekly_total_price = 0
        weekly_total_volume = 0
        weekly_count = 0

        monthly_total_price = 0
        monthly_total_volume = 0
        monthly_count = 0

        yearly_total_price = 0
        yearly_total_volume = 0
        yearly_count = 0

        for energy_price in energy_prices:
            if not energy_price.date:
                continue

            energy_week = energy_price.date.isocalendar().week
            energy_month = energy_price.date.month
            energy_year = energy_price.date.year

            avg_price = CalculationManager.get_average_price_by_energy_price(energy_price, MarketType.BASE, DefaultCurrency.BGN)

            volume = CalculationManager.get_average_volume_by(energy_price, MarketType.BASE)

            if energy_year == current_year:
                yearly_total_price += avg_price
                yearly_total_volume += volume
                yearly_count += 1

            if energy_month == current_month and energy_year == current_year:
                monthly_total_price += avg_price
                monthly_total_volume += volume
                monthly_count += 1

            if energy_week == current_week and energy_year == current_year:
                weekly_total_price += avg_price
                weekly_total_volume += volume
                weekly_count += 1

        weekly_avg_price = weekly_total_price / weekly_count if weekly_count > 0 else 0
        monthly_avg_price = monthly_total_price / monthly_count if monthly_count > 0 else 0
        yearly_avg_price = yearly_total_price / yearly_count if yearly_count > 0 else 0

        return {
            'weekly': {
                'average_price': round(weekly_avg_price, 2),
                'total_volume': round(weekly_total_volume, 2),
            },
            'monthly': {
                'average_price': round(monthly_avg_price, 2),
                'total_volume': round(monthly_total_volume, 2),
            },
            'yearly': {
                'average_price': round(yearly_avg_price, 2),
                'total_volume': round(yearly_total_volume, 2),
            }
        }

    @staticmethod
    def calculate_statistics(energy_prices, contextTitle):
        total_volume = 0
        min_price = float('inf')
        max_price = float('-inf')
        min_volume = float('inf')
        max_volume = float('-inf')
        total_price = 0
        count = 0
        dates = []
        prices = []

        for energy_price in energy_prices:
            date = str(energy_price.date)
            avg_price = CalculationManager.get_average_price_by_energy_price(energy_price, MarketType.BASE, DefaultCurrency.BGN)
            volume = CalculationManager.get_average_volume_by(energy_price, MarketType.BASE)

            total_price += avg_price
            count += 1
            total_volume += volume
            min_price = min(min_price, avg_price)
            max_price = max(max_price, avg_price)
            min_volume = min(min_volume, volume)
            max_volume = max(max_volume, volume)

            dates.append(date)
            prices.append(avg_price)

        avg_price = total_price / count if count > 0 else 0

        return {
            contextTitle: {
                'average_price': f"{round(avg_price, 2)} BGN",
                'total_volume': f"{round(total_volume, 2)} GWh",
                'min_price': f"{min_price} BGN",
                'max_price': f"{max_price} BGN",
                'min_volume': f"{min_volume} GWh",
                'max_volume': f"{max_volume} GWh",
                'dates': dates,
                'prices': prices,
            }
        }
