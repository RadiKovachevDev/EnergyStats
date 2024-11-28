from django.db import models


class EnergyStatistic(models.Model):
    date = models.DateField()
    total_consumption = models.DecimalField(max_digits=10, decimal_places=2)  # kWh
    average_price = models.DecimalField(max_digits=5, decimal_places=2)  # €/kWh
    peak_price = models.DecimalField(max_digits=5, decimal_places=2)  # €/kWh
    lowest_price = models.DecimalField(max_digits=5, decimal_places=2)  # €/kWh

    def __str__(self):
        return f"Statistics for {self.date}"
