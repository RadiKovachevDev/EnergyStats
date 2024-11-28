from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from EnergyStats.stats.models import EnergyStatistic


@login_required
def statistics_view(request):
    stats = EnergyStatistic.objects.all().order_by('-date')
    return render(request, 'stats/stats.html', {'stats': stats})

