import datetime
from collections import defaultdict

from workday.library import make_days
from workday.library import create_block
from datetime import date


def get_workday_from_calculator(calculator):
    begin_service = calculator.start_date
    end_service = calculator.end_date
    today = date.today()

    service_days = make_days.make_service_days(begin_service, end_service)  # 입대 ~ 전역전

    if begin_service < today:
        blocked_service_days = create_block.make_blocked_service_days(today, end_service)  # 입대 ~ 전역
    else:
        blocked_service_days = create_block.make_blocked_service_days(begin_service, end_service)  # 입대 ~ 전역

    serviced_days = make_days.make_serviced_days(begin_service)  # 입대~어제
    remain_days = service_days - serviced_days  # 오늘 ~ 전역전

    leaves = set()  # 휴가
    leaves_list = calculator.leave_set.all()
    for leave in leaves_list:
        leaves.update(leave.get_leaves())

    dayoffs = set()
    dayoff_list = calculator.dayoff_set.all()
    for dayoff in dayoff_list:
        dayoffs.add(dayoff.date)

    workdays = remain_days - dayoffs - leaves  # 실출근

    workdays_list = list(workdays)

    months = insert_None_for_align(blocked_service_days)

    weekdays = ['월', '화', '수', '목', '금', '토', '일']

    if workdays_list:
        end_workday = max(workdays_list)
    else:
        end_workday = end_service

    percent = round(len(serviced_days) / len(service_days) * 100, 2)

    data = {
        'blocked_service_days': zip(months, blocked_service_days),

        'num_service_days': len(service_days),

        'num_workdays': len(workdays),
        'today': today,
        'end_workday': end_workday,
        'workday_percent': f'{(1 - len(workdays) / len(service_days)) * 100 :.2f}',

        'percent': f'{percent :.2f}' if percent <= 100 else "100.00",
        'num_remain_days': len(remain_days),

        'weekdays': weekdays,
        'serviced_days': serviced_days,
        'leaves': leaves,
        'num_leaves': len(leaves),
        'dayoffs': dayoffs,
    }

    return data


def insert_None_for_align(blocked_service_days):
    months = []
    first_weekdays = []
    last_weekdays = []
    for month in blocked_service_days:
        first_weekdays.append(month[0].weekday())
        last_weekdays.append(month[-1].weekday())

        months.append(month[0])

    for i in range(len(blocked_service_days)):
        first_count = first_weekdays[i]
        last_count = 6 - last_weekdays[i]
        for j in range(first_count):
            blocked_service_days[i].insert(0, None)
        for j in range(last_count):
            blocked_service_days[i].append(None)

    return months


def get_workday_from_calculator_light(calculator):
    begin_service = calculator.start_date
    end_service = calculator.end_date

    service_days = make_days.make_service_days(begin_service, end_service)  # 입대 ~ 전역전

    serviced_days = make_days.make_serviced_days(begin_service)  # 입대~어제
    remain_days = service_days - serviced_days  # 오늘 ~ 전역전

    leaves = set()  # 휴가
    leaves_list = calculator.leave_set.all()
    for leave in leaves_list:
        leaves.update(leave.get_leaves())

    dayoffs = set()
    dayoff_list = calculator.dayoff_set.all()
    for dayoff in dayoff_list:
        dayoffs.add(dayoff.date)

    workdays = remain_days - dayoffs - leaves  # 실출근

    workdays_list = list(workdays)

    if workdays_list:
        end_workday = max(workdays_list)
    else:
        end_workday = end_service

    percent = round(len(serviced_days) / len(service_days) * 100, 2)

    data = {
        'num_workdays': len(workdays),
        'end_workday': end_workday,
        'workday_percent': f'{(1 - len(workdays) / len(service_days)) * 100 :.2f}',

        'percent': f'{percent :.2f}' if percent <= 100 else "100.00",
        'num_remain_days': len(remain_days),  #
    }

    return data


def get_workday_from_calculator_barracks(calculator):
    begin_service = calculator.start_date
    end_service = calculator.end_date

    service_days = make_days.make_service_days(begin_service, end_service)  # 입대 ~ 전역전

    serviced_days = make_days.make_serviced_days(begin_service)  # 입대~어제
    remain_days = service_days - serviced_days  # 오늘 ~ 전역전

    leaves = set()  # 휴가
    leaves_list = calculator.leave_set.all()
    for leave in leaves_list:
        leaves.update(leave.get_leaves())

    dayoffs = set()
    dayoff_list = calculator.dayoff_set.all()
    for dayoff in dayoff_list:
        dayoffs.add(dayoff.date)

    workdays = remain_days - dayoffs - leaves  # 실출근

    workdays_list = list(workdays)

    if workdays_list:
        end_workday = max(workdays_list)
    else:
        end_workday = end_service

    percent = round(len(serviced_days) / len(service_days) * 100, 2)

    data = {
        'num_workdays': len(workdays),
        'end_workday': end_workday,
        'workday_percent': round((1 - len(workdays) / len(service_days)) * 100, 2),

        'percent': percent if percent <= 100 else 100.0,
        'num_remain_days': len(remain_days),
    }

    return data


def get_leave_from_calculator(calculator):
    parsed_leaves = defaultdict(int)  # 휴가
    for leave in calculator.leave_set.all():
        parsed_leaves[leave.type] += leave.days().days

    parsed_leaves["total"] = sum(parsed_leaves.values())

    return parsed_leaves


def get_leave_for_progress(sorted_calculator_leave_list, max_leaves):
    for calculator_color, leaves in sorted_calculator_leave_list.items():
        for leave_type, leave in leaves.items():
            percent = leave / max_leaves * 100 if max_leaves else 0
            sorted_calculator_leave_list[calculator_color][leave_type] = (leave, percent)


def get_workday_from_calculator_ranking(calculator):
    begin_service = calculator.start_date
    end_service = calculator.end_date

    service_days = make_days.make_service_days(begin_service, end_service)  # 입대 ~ 전역전

    serviced_days = make_days.make_serviced_days(begin_service)  # 입대~어제
    remain_days = service_days - serviced_days  # 오늘 ~ 전역전

    # 휴가
    leaves = {leave_date for leave in calculator.leave_set.all() for leave_date in leave.get_leaves()}

    # 휴일
    dayoffs = {dayoff.date for dayoff in calculator.dayoff_set.all()}

    # 실출근
    workdays = remain_days - dayoffs - leaves

    end_workday = max(workdays) if workdays else end_service

    percent = round(len(serviced_days) / len(service_days) * 100, 1)

    data = {
        'num_workdays': len(workdays),
        'end_workday': end_workday,
        'workday_percent': round((1 - len(workdays) / len(service_days)) * 100, 1),

        'percent': percent if percent <= 100 else 100.0,
        'num_remain_days': len(remain_days),

        'num_leaves': len(leaves)
    }

    return data
