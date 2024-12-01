from typing import final
from django.db import models
from django.db.models import Sum

from EnergyStats.common.enums import DefaultCurrency, MarketType
from EnergyStats.common.local_data_manager import LocalDataManager
from EnergyStats.energy_service.models import PeakHourConfiguration


@final
class CalculationManager(models.Manager):
    @staticmethod
    def fetch_peak_hour():
        config = PeakHourConfiguration.objects.first()
        if not config or not config.peak_hours:
            raise ValueError("No PeakHourConfiguration or peak hours found in the database.")

        return config.peak_hours

    @staticmethod
    def get_price_by(hourly_info, default_currency):
        price = None
        if default_currency == DefaultCurrency.BGN:
            price = hourly_info.bgn if hourly_info else None
        elif default_currency == DefaultCurrency.EUR:
            price = hourly_info.eur if hourly_info else None
        return round(price, 5)

    @staticmethod
    def get_min_price_by(date, market_type):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()
        if not energy_price:
            raise ValueError(f"No EnergyPrice found for the date {date}.")

        peak_hours = CalculationManager.fetch_peak_hour()

        min_price = float('inf')

        for hourly_data in energy_price.hourly_data.all():
            price = None

            if market_type == MarketType.BASE:
                price = hourly_data.data.bgn if hourly_data.data else None
            elif market_type == MarketType.PEAK:
                if peak_hours and hourly_data.time in peak_hours:
                    price = hourly_data.data.bgn if hourly_data.data else None
            elif market_type == MarketType.OFF_PEAK:
                if peak_hours and hourly_data.time not in peak_hours:
                    price = hourly_data.data.bgn if hourly_data.data else None

            if price is not None and price < min_price:
                min_price = price

        return round(min_price, 2) if min_price != float('inf') else None

    @staticmethod
    def get_max_price_by(date, market_type):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()
        if not energy_price:
            raise ValueError(f"No EnergyPrice found for the date {date}.")

        peak_hours = CalculationManager.fetch_peak_hour()

        max_price = float('-inf')

        for hourly_data in energy_price.hourly_data.all():
            price = None

            if market_type == MarketType.BASE:
                price = hourly_data.data.bgn if hourly_data.data else None
            elif market_type == MarketType.PEAK:
                if peak_hours and hourly_data.time in peak_hours:
                    price = hourly_data.data.bgn if hourly_data.data else None
            elif market_type == MarketType.OFF_PEAK:
                if peak_hours and hourly_data.time not in peak_hours:
                    price = hourly_data.data.bgn if hourly_data.data else None

            if price is not None and price > max_price:
                max_price = price

        return round(max_price, 2) if max_price != float('-inf') else None

    @staticmethod
    def get_min_volume_by(date, market_type):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()
        if not energy_price:
            raise ValueError(f"No EnergyPrice found for the date {date}.")

        peak_hours = CalculationManager.fetch_peak_hour()

        min_volume = float('inf')

        for hourly_data in energy_price.hourly_data.all():
            volume = None

            if market_type == MarketType.BASE:
                volume = hourly_data.data.volume if hourly_data.data else None
            elif market_type == MarketType.PEAK:
                if peak_hours and hourly_data.time in peak_hours:
                    volume = hourly_data.data.volume if hourly_data.data else None
            elif market_type == MarketType.OFF_PEAK:
                if peak_hours and hourly_data.time not in peak_hours:
                    volume = hourly_data.data.volume if hourly_data.data else None

            if volume is not None and volume < min_volume:
                min_volume = volume

        return round(min_volume, 2) if min_volume != float('inf') else None

    @staticmethod
    def get_max_volume_by(date, market_type):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()
        if not energy_price:
            raise ValueError(f"No EnergyPrice found for the date {date}.")

        peak_hours = CalculationManager.fetch_peak_hour()

        max_volume = float('-inf')

        for hourly_data in energy_price.hourly_data.all():
            volume = None

            if market_type == MarketType.BASE:
                volume = hourly_data.data.volume if hourly_data.data else None
            elif market_type == MarketType.PEAK:
                if peak_hours and hourly_data.time in peak_hours:
                    volume = hourly_data.data.volume if hourly_data.data else None
            elif market_type == MarketType.OFF_PEAK:
                if peak_hours and hourly_data.time not in peak_hours:
                    volume = hourly_data.data.volume if hourly_data.data else None

            if volume is not None and volume > max_volume:
                max_volume = volume

        return round(max_volume, 2) if max_volume != float('-inf') else None

    @staticmethod
    def get_total_volume_for_day(date):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()
        if not energy_price:
            raise ValueError(f"No EnergyPrice found for the date {date}.")

        total_volume = energy_price.hourly_data.aggregate(total_volume=Sum('data__volume'))['total_volume']

        return round(total_volume, 2) or 0

    @staticmethod
    def get_average_price_by(date, market_type, default_currency):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()
        if not energy_price:
            raise ValueError(f"No EnergyPrice found for the date {date}.")

        peak_hours = CalculationManager.fetch_peak_hour()

        total_price = 0
        count = 0

        for hourly_data in energy_price.hourly_data.all():
            price = None

            if market_type == MarketType.BASE:
                price = hourly_data.data.bgn if default_currency == DefaultCurrency.BGN else hourly_data.data.eur
            elif market_type == MarketType.PEAK:
                if peak_hours and hourly_data.time in peak_hours:
                    price = hourly_data.data.bgn if default_currency == DefaultCurrency.BGN else hourly_data.data.eur
            elif market_type == MarketType.OFF_PEAK:
                if peak_hours and hourly_data.time not in peak_hours:
                    price = hourly_data.data.bgn if default_currency == DefaultCurrency.BGN else hourly_data.data.eur

            if price is not None:
                total_price += price
                count += 1

        average_price = total_price / count if count > 0 else 0

        return round(average_price, 2)

