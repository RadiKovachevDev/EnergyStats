import time
from datetime import datetime
import calendar
from typing import final

from EnergyStats.common.calculation_manager import CalculationManager
from EnergyStats.common.enums import MarketType, DefaultCurrency, MeasuringUnits
from EnergyStats.common.local_data_manager import LocalDataManager


@final
class StatisticsManager:
    current_date = datetime.now()
    calendar = calendar.Calendar()
    date_formatter = "%d.%m.%Y"

    @staticmethod
    def fetch_weekly_data():
        weekly_data = []
        energy_prices = LocalDataManager.get_energy_prices()

        if not energy_prices:
            return weekly_data

        current_week = StatisticsManager.current_date.isocalendar().week
        current_year = StatisticsManager.current_date.isocalendar().year

        for energy_price in energy_prices:
            if energy_price.date:
                try:
                    energy_date = datetime.strptime(energy_price.date.strftime(StatisticsManager.date_formatter), StatisticsManager.date_formatter)
                    energy_week = energy_date.isocalendar().week
                    energy_year = energy_date.isocalendar().year

                    if energy_week == current_week and energy_year == current_year:
                        weekly_data.append(energy_price)
                except ValueError:
                    continue

        return list(reversed(weekly_data))

    @staticmethod
    def fetch_monthly_data():
        monthly_data = []
        energy_prices = LocalDataManager.get_energy_prices()

        if not energy_prices:
            return monthly_data

        current_month = StatisticsManager.current_date.month
        current_year = StatisticsManager.current_date.year

        for energy_price in energy_prices:
            if energy_price.date:
                try:
                    energy_date = datetime.strptime(energy_price.date.strftime(StatisticsManager.date_formatter), StatisticsManager.date_formatter)
                    if energy_date.month == current_month and energy_date.year == current_year:
                        monthly_data.append(energy_price)
                except ValueError:
                    continue

        return list(reversed(monthly_data))

    @staticmethod
    def fetch_yearly_data():
        yearly_data = []
        energy_prices = LocalDataManager.get_energy_prices()

        if not energy_prices:
            return yearly_data

        current_year = StatisticsManager.current_date.year

        for energy_price in energy_prices:
            if energy_price.date:
                try:
                    energy_date = datetime.strptime(energy_price.date.strftime(StatisticsManager.date_formatter), StatisticsManager.date_formatter)
                    if energy_date.year == current_year:
                        yearly_data.append(energy_price)
                except ValueError:
                    continue

        return list(reversed(yearly_data))

    @staticmethod
    def days_in_current_month():
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        _, number_of_days = calendar.monthrange(year, month)
        return number_of_days

    @staticmethod
    def average_price_by(energy_prices, market_type=MarketType.BASE):
        total_price = 0.0
        count = 0.0
        if not isinstance(energy_prices, list):
            energy_prices = [energy_prices]

        for energy_price in energy_prices:
            try:
                average_price = CalculationManager.get_average_price_by(energy_price.date, market_type, DefaultCurrency.BGN)
                if average_price is not None:
                    total_price += average_price
                    count += 1.0
            except ValueError:
                continue

        if total_price > 0 and count > 0:
            return round(total_price / count, 2)
        else:
            return 0.0

    @staticmethod
    def average_volume_by(energy_prices, market_type=MarketType.BASE):
        total_volume = 0.0
        count = 0.0

        if not isinstance(energy_prices, list):
            energy_prices = [energy_prices]

        for energy_price in energy_prices:
            try:
                average_volume = CalculationManager.get_average_volume_by(energy_price, market_type)
                if average_volume is not None:
                    total_volume += average_volume
                    count += 1.0
            except ValueError:
                continue

        if total_volume > 0 and count > 0:
            return round(total_volume / count, 2)
        else:
            return 0.0

    import time

    @staticmethod
    def total_volume_by(energy_prices, measuring_units=MeasuringUnits.MWH, market_type=MarketType.BASE):
        start_time = time.time()  # Започваме да засичаме времето
        print("Start total_volume_by")

        total_volume = 0.0

        for energy_price in energy_prices:
            try:
                volume = CalculationManager.get_total_volume_by(energy_price, market_type)
                if volume is not None:
                    total_volume += volume
            except ValueError:
                continue

        if measuring_units == MeasuringUnits.KWH:
            result = round(total_volume * 1000, 2)
        elif measuring_units == MeasuringUnits.MWH:
            result = round(total_volume, 2)
        elif measuring_units == MeasuringUnits.GWH:
            result = round(total_volume / 1000, 2)
        elif measuring_units == MeasuringUnits.TWH:
            result = round(total_volume / 1_000_000, 2)
        else:
            result = 0.0

        end_time = time.time()
        print(f"End total_volume_by - Execution time: {end_time - start_time:.2f} seconds")

        return result

    @staticmethod
    def min_price_by(energy_prices, market_type=MarketType.BASE):
        min_price = float('inf')

        for energy_price in energy_prices:
            try:
                price = CalculationManager.get_min_price_by(energy_price.date, market_type)
                if price is not None and price < min_price:
                    min_price = price
            except ValueError:
                continue

        return round(min_price, 2) if min_price != float('inf') else 0.0

    @staticmethod
    def min_volume_by(energy_prices, market_type=MarketType.BASE):
        min_volume = float('inf')

        for energy_price in energy_prices:
            try:
                volume = CalculationManager.get_min_volume_by(energy_price.date, market_type)
                if volume is not None and volume < min_volume:
                    min_volume = volume
            except ValueError:
                continue

        return round(min_volume, 2) if min_volume != float('inf') else 0.0

    @staticmethod
    def max_price_by(energy_prices, market_type=MarketType.BASE):
        max_price = float('-inf')

        for energy_price in energy_prices:
            try:
                price = CalculationManager.get_max_price_by(energy_price.date, market_type)
                if price is not None and price > max_price:
                    max_price = price
            except ValueError:
                continue

        return round(max_price, 2) if max_price != float('-inf') else 0.0

    @staticmethod
    def max_volume_by(energy_prices, market_type=MarketType.BASE):
        max_volume = float('-inf')

        for energy_price in energy_prices:
            try:
                volume = CalculationManager.get_max_volume_by(energy_price.date, market_type)
                if volume is not None and volume > max_volume:
                    max_volume = volume
            except ValueError:
                continue

        return round(max_volume, 2) if max_volume != float('-inf') else 0.0
