from django.core.management.base import BaseCommand, CommandError

from workday.models import Calculator
from rank.models import RankingChart

from workday.library import calculator_lib


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            calculator_list = Calculator.objects.iterator()

            for calculator in calculator_list:
                info = calculator_lib.get_workday_from_calculator_ranking(calculator)
                obj, is_created = RankingChart.objects.update_or_create(
                    calculator=calculator,
                    defaults={
                        'start_date': calculator.start_date,
                        'end_date': calculator.end_date,
                        'end_workday': info['end_workday'],

                        'num_remaindays': info['num_remain_days'],
                        'num_workdays': info['num_workdays'],
                        'num_leaves': info['num_leaves'],

                        'percent': info['percent'],
                        'workday_percent': info['workday_percent']
                    }

                )

                if is_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Calculator ranking was created at {calculator.name}."))
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Calculator ranking was updated at {calculator.name}."))

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f'CommandError was raised.{error}'))
            return

        self.stdout.write(self.style.SUCCESS('Ranking chart successfully updated.'))
        return
