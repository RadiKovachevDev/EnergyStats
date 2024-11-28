from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from EnergyStats.prices.models import ElectricityPrice


@login_required
def price_list(request):
    prices = ElectricityPrice.objects.all().order_by('-date')
    return render(request, 'prices/price_list.html', {'prices': prices})
