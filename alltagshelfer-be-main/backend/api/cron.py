# api/cron.py

from .models import BlacklistedTokens
from django_cron import CronJobBase, Schedule
from django.utils import timezone


class DeleteExpiredTokens(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.cron'

    def do(self):
        # Delete Blacklisted tokens whose expiry datetime is lower than now
        BlacklistedTokens.objects.filter(
            expiration_datetime__lt=timezone.now()).delete()
        # DEBUG (DELETE ALL): BlacklistedTokens.objects.all().delete()
