from django.core.management.base import BaseCommand

from converter_app.models import CurrencyRate
from converter_app.utils import upload_rates


class Command(BaseCommand):
    help = 'Fill DB by rates for first app start'

    def handle(self, *args, **options):
        if CurrencyRate.objects.exists():
            self.stdout.write('Rates first load: rates already exists')
            return

        upload_rates()

        self.stdout.write('Rates first load: rates successfully loaded')
