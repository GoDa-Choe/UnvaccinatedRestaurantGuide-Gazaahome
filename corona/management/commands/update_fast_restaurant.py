from django.core.management.base import BaseCommand, CommandError

from corona.models import FastRestaurant, Restaurant


class Command(BaseCommand):

    def update_or_create_fast_restaurant(self, restaurant):
        base = restaurant
        data = self.parsing_restaurant(restaurant)
        fast_restaurant, created = FastRestaurant.objects.update_or_create(name=base, defaults=data)

        if created:
            self.stdout.write(self.style.SUCCESS(f"{fast_restaurant.pk} | {fast_restaurant.name} | Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"{fast_restaurant.pk} | {fast_restaurant.name} | Updated"))

    @staticmethod
    def parsing_restaurant(restaurant):
        data = {
            'name': restaurant.name,
            'address': restaurant.address,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,

            'verifieded': restaurant.verifieded,

            'url': restaurant.url,

            'category': restaurant.category.name,
            'tags': " ".join(restaurant.tags.values_list('name', flat=True)[:4]),
            'unvaccinated_pass': restaurant.unvaccinated_pass.type,

            # likes and dislikes and comments
            'num_likes': restaurant.num_likes(),
            'num_dislikes': restaurant.num_dislikes(),
            'num_comments': restaurant.num_comments(),
            'num_hits': restaurant.hit_count.hits,
        }

        return data

    def handle(self, *args, **options):
        try:
            for fast in FastRestaurant.objects.iterator():
                fast.delete()

            for restaurant in Restaurant.objects.iterator():
                self.update_or_create_fast_restaurant(restaurant)

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f'CommandError was raised. {error}'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'{FastRestaurant.objects.count()} / {Restaurant.objects.count()} Successfully Updated and Created.'))
        return
