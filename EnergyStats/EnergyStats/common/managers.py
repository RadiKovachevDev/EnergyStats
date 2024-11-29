from django.db import models


class LocalDataManager(models.Manager):
    def get_peak_hours(self, date):
        prices = self.filter(date=date).prefetch_related('hourly_data__data')
        peak_hours = []
        for price in prices:
            for hourly_data in price.hourly_data.all():
                hour = int(hourly_data.time.split(":")[0])
                if 9 <= hour <= 19:
                    peak_hours.append(hourly_data)
        return peak_hours

    def get_off_peak_hours(self, date):
        prices = self.filter(date=date).prefetch_related('hourly_data__data')
        off_peak_hours = []
        for price in prices:
            for hourly_data in price.hourly_data.all():
                hour = int(hourly_data.time.split(":")[0])
                if hour < 9 or hour > 19:
                    off_peak_hours.append(hourly_data)
        return off_peak_hours
