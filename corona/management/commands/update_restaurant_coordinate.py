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

                if not first_match:
                    self.stdout.write(self.style.SUCCESS(
                        f"      {restaurant.pk} | {restaurant.name} | {restaurant.address} | None,  None."))
                    continue

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


