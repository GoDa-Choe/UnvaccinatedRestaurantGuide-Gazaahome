import datetime
from workday.library import holidays


def make_days(begin, end):
    days = set()
    current = begin
    while current < end:
        days.add(current)
        current += datetime.timedelta(days=1)
    return days


def make_days_light(begin, end):
    days = set(range(begin, end, datetime.timedelta(days=1)))
    current = begin
    while current < end:
        days.add(current)
        current += datetime.timedelta(days=1)
    return days


def make_service_days(begin_service, end_service):
    service_days = make_days(begin_service, end_service)
    return service_days


def make_serviced_days(begin):
    serviced_days = make_days(begin, datetime.date.today())
    return serviced_days


def get_holidays():
    return holidays.holidays_2019 | holidays.holidays_2020 | holidays.holidays_2021 | holidays.holidays_2022 | holidays.holidays_2023


def get_weekends(begin, end):
    return holidays.weekend(begin, end)
