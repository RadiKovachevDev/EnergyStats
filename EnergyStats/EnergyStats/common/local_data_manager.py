from typing import final
from django.db import models
from EnergyStats.common.enums import MarketType
from EnergyStats.energy_service.models import EnergyPrice, PeakHourConfiguration
from django.utils.timezone import localtime


@final
class LocalDataManager(models.Manager):

    @staticmethod
    def get_energy_prices():
        return EnergyPrice.objects.all()

    @staticmethod
    def get_energy_price(date):
        return EnergyPrice.objects.filter(date=date)

    @staticmethod
    def get_hours_by(date, market_type):
        config = PeakHourConfiguration.objects.first()
        if not config:
            raise ValueError("No PeakHourConfiguration found in the database.")
        prices = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data')
        filtered_hours = []
        if market_type == MarketType.PEAK:
            for price in prices:
                for hourly_data in price.hourly_data.all():
                    if hourly_data.time in config.peak_hours:
                        filtered_hours.append(hourly_data)
        elif market_type == MarketType.OFF_PEAK:
            for price in prices:
                for hourly_data in price.hourly_data.all():
                    if hourly_data.time not in config.peak_hours:
                        filtered_hours.append(hourly_data)
        elif market_type == MarketType.BASE:
            for price in prices:
                for hourly_data in price.hourly_data.all():
                    filtered_hours.append(hourly_data)
        else:
            raise ValueError(f"Invalid market_type: {market_type}")

        return filtered_hours

    @staticmethod
    def get_hourly_info_for_current_hour(date):
        energy_price = LocalDataManager.get_energy_price(date).prefetch_related('hourly_data__data').first()

        if not energy_price:
            return None

        current_time = localtime().strftime("%H:00:00")
        hourly_data = energy_price.hourly_data.filter(time=current_time).first()
        if hourly_data:
            return hourly_data.data
        return None


