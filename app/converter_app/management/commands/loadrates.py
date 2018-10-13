from django.core.management.base import BaseCommand

from converter_app.models import CurrencyRate
from converter_app.utils import load_rates


class Command(BaseCommand):
    help = 'Fill DB by rates for first time'

    def handle(self, *args, **options):
        if CurrencyRate.objects.exists():
            self.stdout.write('Rates already exists')
            return

        load_rates()

        self.stdout.write('Rates successfully loaded')
