from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EnergyStats.accounts.urls')),
    path('', include('EnergyStats.dashboard.urls')),
    path('prices/', include('EnergyStats.prices.urls')),
    path('statistics/', include('EnergyStats.stats.urls')),
    path('energy-service/', include('EnergyStats.energy_service.urls')),
]
