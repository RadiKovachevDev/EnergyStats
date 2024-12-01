from django.contrib import admin
from .models import HourlyInfo, HourlyData, EnergyPrice, LatestPriceDate, PeakHourConfiguration

admin.site.register(HourlyInfo)
admin.site.register(HourlyData)
admin.site.register(EnergyPrice)
admin.site.register(LatestPriceDate)


@admin.register(PeakHourConfiguration)
class PeakHourConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_peak_hours')
    fields = ('peak_hours',)
    readonly_fields = ()
    actions = None

    def display_peak_hours(self, obj):
        return ", ".join(obj.peak_hours)
    display_peak_hours.short_description = "Peak Hours"
