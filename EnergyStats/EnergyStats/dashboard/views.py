from datetime import date
from django.shortcuts import render
from EnergyStats.energy_service.models import EnergyPrice


def dashboard_view(request):
    today = date.today()

    peak_hours = EnergyPrice.local_data.get_peak_hours(today)
    off_peak_hours = EnergyPrice.local_data.get_off_peak_hours(today)

    context = {
        'peak_hours': peak_hours,
        'off_peak_hours': off_peak_hours,
        'today': today,
    }
    return render(request, 'dashboard/dashboard.html', context)

