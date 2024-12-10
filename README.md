# EnergyStats
Statistics for free energy market

ТРЯБВА ДА СТАРТИРАТЕ CRON СЪС ОТ SHELL КОНЗОЛАТА И ДА СИ НАПРАВИТЕ МИГРАЦИИ
from .cron import UpdatePricesCronJob
job = UpdatePricesCronJob()
job.do()