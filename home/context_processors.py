from home.models import Corona


def get_corona_decided_count(request):
    today_yesterday = Corona.objects.order_by("-state_date")[:2]
    if len(today_yesterday) == 2:
        today, yesterday = today_yesterday

        return {
            "decided_count": today.decided_count,
            "today_decided_count": today.decided_count - yesterday.decided_count,
        }

    return {
        "decided_count": 0,
        "today_decided_count": 0,
    }
