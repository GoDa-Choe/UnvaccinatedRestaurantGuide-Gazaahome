from datetime import date, timedelta


def make_blocked_service_days(start, end):
    result = [[start], ]
    current = start + timedelta(days=1)
    while current <= end:
        if result[-1][-1].month == current.month:
            result[-1].append(current)
        else:
            result.append([])
            result[-1].append(current)
        current = current + timedelta(days=1)

    return result
