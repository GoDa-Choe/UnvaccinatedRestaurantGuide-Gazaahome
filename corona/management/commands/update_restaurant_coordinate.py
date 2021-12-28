from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils.text import slugify

from openpyxl import load_workbook

from corona.models import Restaurant, RestaurantCategory, UnvaccinatedPass, RestaurantTag

import requests
from urllib.parse import urlparse


class Command(BaseCommand):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    header = {'Authorization': 'KakaoAK 1a1d8745de102eaf124ca7d9d58ed33f'}

    def add_arguments(self, parser):
        parser.add_argument('start_pk', type=int)
        parser.add_argument('end_pk', type=int)

    def get_address(self):
        pass

    def handle(self, *args, **options):
        try:
            start_pk = options['start_pk']
            end_pk = options['end_pk']

            pk_list = [pk for pk in range(start_pk, end_pk + 1)]
            self.stdout.write(self.style.SUCCESS(f"Total: {len(pk_list)}."))

            restaurant_list = Restaurant.objects.filter(pk__in=pk_list).exclude(address__isnull=True).filter(
                latitude__isnull=True).filter(longitude__isnull=True)
            self.stdout.write(self.style.SUCCESS(f"No coorindates: {restaurant_list.count()}."))

            update_required_restaurant_list = []
            for restaurant in restaurant_list:
                address = restaurant.address
                query = f"?query={address}"
                request = self.url + query

                response = requests.get(urlparse(request).geturl(), headers=self.header).json()
                doc = response['documents']

                if not doc:  # no matching results
                    self.stdout.write(self.style.SUCCESS(
                        f"      {restaurant.pk} | {restaurant.name} | {restaurant.address} | None,  None."))
                    continue

                first_match = response['documents'][0]['road_address']
                restaurant.latitude = float(first_match['y'])
                restaurant.longitude = float(first_match['x'])

                self.stdout.write(self.style.SUCCESS(
                    f"      {restaurant.pk} | {restaurant.name} | {restaurant.address} | {restaurant.latitude}, {restaurant.longitude}."))

                update_required_restaurant_list.append(restaurant)

            self.stdout.write(self.style.SUCCESS(f"Matched: {len(update_required_restaurant_list)}."))

            total_updated = 0
            command = input("Update(y)/Cancle(n)-> ")

            if command == "y":
                for update_required_restaurant in update_required_restaurant_list:
                    update_required_restaurant.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"      Update Success {update_required_restaurant.pk} | {update_required_restaurant.name} | {update_required_restaurant.address} | {update_required_restaurant.latitude}, {update_required_restaurant.longitude}."))
                    total_updated += 1

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f'CommandError was raised. {error}'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'Updated: {total_updated}.'))
        return

    # try:
    #     root = Path('corona/management/commands/data/')
    #     file_path = root / options['file_name']
    #
    #     load_wb = load_workbook(file_path, data_only=True)
    #
    #     load_ws = load_wb[options['type']]
    #
    #     for row in load_ws.rows:
    #
    #         if row[0].value in [None, 'no']:
    #             continue
    #
    #         name = row[1].value
    #         address = row[2].value
    #         latitude = row[3].value
    #         longitude = row[4].value
    #         verifieded = True if row[5].value == "TRUE" else False
    #         url = row[6].value
    #
    #         author = self.goda
    #
    #         category, _ = RestaurantCategory.objects.get_or_create(
    #             name=row[7].value,
    #             defaults={
    #                 'slug': slugify(row[7].value, allow_unicode=True)
    #             }
    #         )
    #
    #         if options['type'] == "available":
    #             unvaccinated_pass = UnvaccinatedPass.objects.get(type="미접종 친절")
    #         else:
    #             unvaccinated_pass = UnvaccinatedPass.objects.get(type="미접종 거부")
    #
    #         restaurant, is_created = Restaurant.objects.update_or_create(
    #             name=name,
    #             defaults={
    #                 'address': address,
    #                 'latitude': latitude,
    #                 'longitude': longitude,
    #                 'verifieded': verifieded,
    #                 'url': url,
    #                 'author': author,
    #                 'category': category,
    #                 'unvaccinated_pass': unvaccinated_pass,
    #             }
    #         )
    #
    #         if not is_created:
    #             restaurant.tags.clear()
    #
    #         tags_str = row[10].value
    #         if tags_str:
    #             tags_str = tags_str.strip(' #')
    #             tags_str = tags_str.replace(',', '#')
    #             tags_list = tags_str.split('#')
    #
    #             for tag in tags_list:
    #                 tag = tag.strip()
    #                 tag, is_tag_created = RestaurantTag.objects.get_or_create(name=tag)
    #                 if is_tag_created:
    #                     tag.slug = slugify(tag, allow_unicode=True)
    #                     tag.save()
    #                 restaurant.tags.add(tag)
    #
    #         self.stdout.write(self.style.SUCCESS(f"{name} is created and updated."))
    #         count += 1
    #
    # except CommandError as error:
    #     self.stdout.write(self.style.ERROR(f'CommandError was raised. {error}'))
    #     return
    #
    # self.stdout.write(self.style.SUCCESS(f'{count} Restaurants are created and updated successfully.'))
    # return
