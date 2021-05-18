import datetime


def make_blocked_service_days(service_days, begin_service, end_service):
    count = ((end_service.year - begin_service.year) * 12 + end_service.month) \
            - begin_service.month + 1
    blocked_service_days = [sorted(create_block(service_days, begin_service, th=i)) for i in range(1, count + 1)]
    blocked_service_days[-1].append(end_service)
    return blocked_service_days


def create_block(service, start, th):
    if th == 1:
        pivot_begin = start
    else:
        b_year = start.year
        b_month = start.month + th - 1
        if b_month > 12:
            b_year += 1
            b_month -= 12
        pivot_begin = datetime.date(b_year, b_month, 1)

    e_year = start.year
    e_month = start.month + th
    if e_month > 12:
        e_year += 1
        e_month -= 12
    pivot_end = datetime.date(e_year, e_month, 1)

    result = []
    for date in service:
        if pivot_begin <= date < pivot_end:
            result.append(date)

    return result
