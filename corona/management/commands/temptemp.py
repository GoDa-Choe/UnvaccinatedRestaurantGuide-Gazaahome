from django.core.management.base import BaseCommand, CommandError

from corona.models import FastRestaurant, Restaurant


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            for restaurant in Restaurant.objects.iterator():
                if restaurant.region == "세종특별자치시":
                    restaurant.update(region="세종")
                    restaurant.save()
                elif restaurant.region == "제주특별자치도":
                    restaurant.update(region="제주")

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f'CommandError was raised. {error}'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'{FastRestaurant.objects.count()} / {Restaurant.objects.count()} Successfully Updated and Created.'))
        return
