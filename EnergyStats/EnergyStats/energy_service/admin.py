from django.contrib import admin
from .models import HourlyInfo, HourlyData, EnergyPrice, LatestPriceDate

admin.site.register(HourlyInfo)
admin.site.register(HourlyData)
admin.site.register(EnergyPrice)
admin.site.register(LatestPriceDate)
