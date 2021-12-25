from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils.text import slugify

from openpyxl import load_workbook

from corona.models import Restaurant, RestaurantCategory, UnvaccinatedPass, RestaurantTag


class Command(BaseCommand):
    goda = User.objects.get(is_superuser=True)

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('type', type=str, help='available or unavailable')

    def handle(self, *args, **options):
        count = 0

        try:
            root = Path('corona/management/commands/data/')
            file_path = root / options['file_name']

            load_wb = load_workbook(file_path, data_only=True)

            load_ws = load_wb[options['type']]

            for row in load_ws.rows:

                if row[0].value in [None, 'no']:
                    continue

                name = row[1].value
                address = row[2].value
                latitude = row[3].value
                longitude = row[4].value
                verifieded = True if row[5].value == "TRUE" else False
                url = row[6].value

                author = self.goda

                category, _ = RestaurantCategory.objects.get_or_create(
                    name=row[7].value,
                    defaults={
                        'slug': slugify(row[7].value, allow_unicode=True)
                    }
                )

                if options['type'] == "available":
                    unvaccinated_pass = UnvaccinatedPass.objects.get(type="미접종 친절")
                else:
                    unvaccinated_pass = UnvaccinatedPass.objects.get(type="미접종 거부")

                restaurant, is_created = Restaurant.objects.get_or_create(
                    name=name,
                    defaults={
                        'address': address,
                        'latitude': latitude,
                        'longitude': longitude,
                        'verifieded': verifieded,
                        'url': url,
                        'author': author,
                        'category': category,
                        'unvaccinated_pass': unvaccinated_pass,
                    }
                )

                if not is_created:
                    restaurant.tags.clear()

                tags_str = row[10].value
                if tags_str:
                    tags_str = tags_str.strip(' #')
                    tags_str = tags_str.replace(',', '#')
                    tags_list = tags_str.split('#')

                    for tag in tags_list:
                        tag = tag.strip()
                        tag, is_tag_created = RestaurantTag.objects.get_or_create(name=tag)
                        if is_tag_created:
                            tag.slug = slugify(tag, allow_unicode=True)
                            tag.save()
                        restaurant.tags.add(tag)

                self.stdout.write(self.style.SUCCESS(f"{name} is created and updated."))
                count += 1

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f'CommandError was raised. {error}'))
            return

        self.stdout.write(self.style.SUCCESS(f'{count} Restaurants are created and updated successfully.'))
        return
