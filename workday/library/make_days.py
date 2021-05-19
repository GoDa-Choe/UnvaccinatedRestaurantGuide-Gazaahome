import datetime
from workday.library import holidays


def make_days(begin, end):
    days = set()
    current = begin
    while current != end:
        days.add(current)
        current += datetime.timedelta(days=1)
    return days


def make_service_days(begin_service, end_service):
    service_days = make_days(begin_service, end_service)
    return service_days


def make_serviced_days(begin):
    serviced_days = make_days(begin, datetime.date.today())
    return serviced_days


def make_work_days(service_days):
    days_off = holidays.holidays_2021 | holidays.holidays_2022
    days_off = days_off | holidays.weekends_2021 | holidays.weekends_2022
    days_off = days_off | holidays.leaves | holidays.off_the_clock | holidays.combat_closed

    work_days = service_days - days_off
    return work_days


def get_holidays():
    return holidays.holidays_2021 | holidays.holidays_2022


def get_weekends():
    return holidays.weekends_2021 | holidays.weekends_2022
