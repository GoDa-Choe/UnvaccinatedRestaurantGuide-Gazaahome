from django.core.management.base import BaseCommand, CommandError
from datetime import date

from home.models import Statistics

from django.contrib.auth.models import User
from forum.models import Post, Comment
from workday.models import Calculator, Leave
from barracks.models import Barracks, GuestBook
from troop_review.models import Troop, Review


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:

            today_status = {
                "state_date": date.today(),

                "user_count": User.objects.count(),

                "calculator_count": Calculator.objects.count(),
                "leave_count": Leave.objects.count(),

                "barracks_count": Barracks.objects.count(),
                "guest_book_count": GuestBook.objects.count(),

                "troop_count": Troop.objects.count(),
                "review_count": Review.objects.count(),

                "post_count": Post.objects.count(),
                "comment_count": Comment.objects.count(),

                "user_increment": 0,
                "calculator_increment": 0,
            }

            if yesterday_status := Statistics.objects.last():
                increments = {
                    "user_increment": today_status["user_count"] - yesterday_status.user_count,
                    "calculator_increment": today_status["calculator_count"] - yesterday_status.calculator_count,
                }
                today_status.update(increments)

            Statistics.objects.create(**today_status)

            self.stdout.write(self.style.SUCCESS(f"A Statistics status was created at {today_status['state_date']}."))

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f'CommandError was raised.{error}'))
            return

        self.stdout.write(self.style.SUCCESS('A Statistics status successfully saved.'))
        return
