from django_cron import CronJobBase, Schedule
from .services import update_prices
import logging

logger = logging.getLogger(__name__)


class UpdatePricesCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'energy_service.update_prices_cron'

    def do(self):
        print("Running UpdatePricesCronJob...")
        logger.info("UpdatePricesCronJob started.")
        update_prices()
        logger.info("UpdatePricesCronJob finished.")
