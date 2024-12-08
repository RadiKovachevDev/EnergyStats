from django.db import models


class MarketType(models.TextChoices):
    BASE = 'base', 'Base'
    PEAK = 'peak', 'Peak'
    OFF_PEAK = 'off-peak', 'Off-Peak'


class DefaultCurrency(models.TextChoices):
    BGN = 'BGN', 'BGN'
    EUR = 'EUR', 'EUR'


class MeasuringUnits(models.TextChoices):
    KWH = 'KMh', 'KMh'
    MWH = 'MWh', 'MWh'
    GWH = 'GWh', 'GWh'
    TWH = 'TWh', 'TWh'

