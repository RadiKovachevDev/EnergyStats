from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from EnergyStats.common.local_data_manager import LocalDataManager


@login_required
def prices_view(request):
    prices = LocalDataManager.get_energy_prices()

    context = {
        'prices': prices
    }
    return render(request, 'prices/prices.html', context)
