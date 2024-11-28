from django.db import models


class ElectricityPrice(models.Model):
    date = models.DateField()
    price_per_kwh = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date}: {self.price_per_kwh} €/kWh"
