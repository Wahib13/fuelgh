from django.core.management.base import BaseCommand

from fuelprices.tasks import update_prices


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_prices()
