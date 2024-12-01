from django.db import models


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


class LatestPriceDate(models.Model):
    latest_date = models.DateField()

    def __str__(self):
        return f"Latest Date: {self.latest_date}"

from django.db import models


class PeakHourConfiguration(models.Model):
    DEFAULT_PEAK_HOURS = [
        "08:00:00", "09:00:00", "10:00:00", "11:00:00", "12:00:00",
        "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00",
        "18:00:00", "19:00:00"
    ]

    peak_hours = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.peak_hours:
            self.peak_hours = self.DEFAULT_PEAK_HOURS
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Peak Hours: {', '.join(self.peak_hours)}"
