from datetime import date
import requests
import xml.etree.ElementTree as ElementTree

from django.core.management.base import BaseCommand
from home.models import Corona


class Command(BaseCommand):
    help = "Get and Save today's corona decided count"
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
    queryParams = {
        'ServiceKey': "8UwAerzEyzQU2dqQfQClwPsIdutSvl1oNGoD5AcTzWiAGbOYGiaxBw6d93wQgFup2H2C/rb8jn7ku/1+Qabp6Q==",
        'pageNo': '1',
        'numOfRows': '10',
        'startCreateDt': '',
        'endCreateDt': '',
    }

    @staticmethod
    def _found(root):
        total_count = root.find("body").find("totalCount").text
        return bool(total_count)

    @staticmethod
    def _get_decide_count(root):
        decide_count = root.find("body").find("items").find("item").find("decideCnt").text
        return int(decide_count)

    def _get_response_root(self, today):

        self.queryParams["startCreateDt"] = today.strftime("%Y%m%d")
        self.queryParams["endCreateDt"] = today.strftime("%Y%m%d")

        response = requests.get(self.url, params=self.queryParams)
        root = ElementTree.fromstring(response.text)
        return root

    def handle(self, *args, **options):
        try:
            today = date.today()
            root = self._get_response_root(today)

            if self._found(root) and not Corona.objects.filter(state_date=today):
                decided_count = self._get_decide_count(root)

                Corona.objects.create(state_date=today, decided_count=decided_count)
                self.stdout.write(
                    self.style.SUCCESS(f"new corona decide count was finded at {today}({decided_count})."))
        except AttributeError:
            self.stdout.write(self.style.ERROR(f'AttributeError was raised.{date.today()}'))
            return

        self.stdout.write(self.style.SUCCESS('Successfully saved.'))
        return
