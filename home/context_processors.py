from home.models import Corona
from corona.models import Post
from django.contrib.auth.models import User
import os


def get_corona_decided_count(request):
    today_yesterday = Corona.objects.order_by("-state_date")[:2]
    id = os.environ.get('NOTIFICATION_ID', None)

    notification = Post.objects.get(pk=int(id)) if id is not None else None

    if len(today_yesterday) == 2:
        today, yesterday = today_yesterday

        return {
            "decided_count": today.decided_count,
            "today_decided_count": today.decided_count - yesterday.decided_count,
            "notification": notification
        }

    return {
        "decided_count": 0,
        "today_decided_count": 0,
        "notification": notification
    }
