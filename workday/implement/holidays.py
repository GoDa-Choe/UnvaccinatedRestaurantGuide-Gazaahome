from datetime import date, timedelta

holidays_2021 = {
    date(2021, 1, 1),  # 새해
    date(2021, 2, 11), date(2021, 2, 12), date(2021, 2, 13),  # 설
    date(2021, 3, 1),  # 삼일절
    date(2021, 5, 5),  # 어린이날
    date(2021, 5, 19),  # 석가탄신일
    date(2021, 6, 6),  # 현충일
    date(2021, 8, 15),  # 광복절
    date(2021, 9, 20), date(2021, 9, 21), date(2021, 9, 22),  # 추석
    date(2021, 10, 3),  # 개천절
    date(2021, 10, 9),  # 한글날
    date(2021, 12, 25),  # 크리스마스
}

holidays_2022 = {
    date(2021, 1, 1),  # 새해
    date(2021, 2, 1), date(2021, 2, 2), date(2021, 2, 3),  # 설
    date(2021, 3, 1),  # 삼일절
    date(2021, 5, 5),  # 어린이날
    date(2021, 5, 8),  # 석가탄신일
    date(2021, 6, 6),  # 현충일
    date(2021, 8, 15),  # 광복절
    date(2021, 9, 9), date(2021, 9, 10), date(2021, 9, 11), date(2021, 9, 12),  # 추석
    date(2021, 10, 3),  # 개천절
    date(2021, 10, 9),  # 한글날
    date(2021, 12, 25),  # 크리스마스
}


def weekend(year):
    weekends = set()

    begin = date(year, 1, 1)
    end = date(year, 12, 31)

    current = begin
    while current <= end:
        if current.weekday() in [5, 6]:
            weekends.add(current)
        current += timedelta(days=1)

    return weekends


weekends_2021 = weekend(2021)
weekends_2022 = weekend(2022)

leaves = set()  # later implement
off_the_clock = set()  # later implement
combat_closed = set()  # later implement
