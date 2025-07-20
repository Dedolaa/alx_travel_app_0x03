from django.core.management.base import BaseCommand
from listings.models import Listing
from faker import Faker   # type: ignore
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        fake = Faker()
        Listing.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted old listings'))

        for _ in range(10):
            Listing.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(),
                location=fake.city(),
                price_per_night=round(random.uniform(50, 500), 2),
                available=True
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded listings'))
