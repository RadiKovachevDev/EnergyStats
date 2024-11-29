from django.db import models

from EnergyStats.common.managers import LocalDataManager


class HourlyInfo(models.Model):
    eur = models.FloatField()
    bgn = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return f"EUR: {self.eur}, BGN: {self.bgn}, Volume: {self.volume}"


class HourlyData(models.Model):
    time = models.CharField(max_length=50)
    data = models.OneToOneField(HourlyInfo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Time: {self.time}, Data: {self.data}"


class EnergyPrice(models.Model):
    _id = models.CharField(max_length=50, primary_key=True)
    date = models.DateField(null=True, blank=True)
    hourly_data = models.ManyToManyField(HourlyData)

    objects = models.Manager()
    local_data = LocalDataManager()


class LatestPriceDate(models.Model):
    latest_date = models.DateField()

    def __str__(self):
        return f"Latest Date: {self.latest_date}"
