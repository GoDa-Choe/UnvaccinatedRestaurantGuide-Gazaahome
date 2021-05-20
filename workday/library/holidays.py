from datetime import date, timedelta

holidays_2019 = {
    date(2019, 1, 1),  # 새해
    date(2019, 2, 4), date(2019, 2, 5), date(2019, 2, 6),  # 설
    date(2019, 3, 1),  # 삼일절
    date(2019, 5, 5), date(2019, 5, 6),  # 어린이날/대체휴일
    date(2019, 5, 12),  # 석가탄신일
    date(2019, 6, 6),  # 현충일
    date(2019, 8, 15),  # 광복절
    date(2019, 9, 12), date(2019, 9, 13), date(2019, 9, 14),  # 추석
    date(2019, 10, 3),  # 개천절
    date(2019, 10, 9),  # 한글날
    date(2019, 12, 25),  # 크리스마스
}

holidays_2020 = {
    date(2020, 1, 1),  # 새해
    date(2020, 1, 24), date(2020, 1, 25), date(2020, 1, 26), date(2020, 1, 27),  # 설
    date(2020, 3, 1),  # 삼일절
    date(2020, 4, 30),  # 석가탄신일
    date(2020, 5, 5),  # 어린이날
    date(2020, 6, 6),  # 현충일
    date(2020, 8, 15), date(2020, 8, 17),  # 광복절/대체휴일
    date(2020, 9, 30), date(2020, 10, 1), date(2020, 10, 2),  # 추석
    date(2020, 10, 3),  # 개천절
    date(2020, 10, 9),  # 한글날
    date(2020, 12, 25),  # 크리스마스
}

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
    date(2022, 1, 1),  # 새해
    date(2022, 2, 1), date(2022, 2, 2), date(2022, 2, 3),  # 설
    date(2022, 3, 1),  # 삼일절
    date(2022, 5, 5),  # 어린이날
    date(2022, 5, 8),  # 석가탄신일
    date(2022, 6, 6),  # 현충일
    date(2022, 8, 15),  # 광복절
    date(2022, 9, 9), date(2022, 9, 10), date(2022, 9, 11), date(2022, 9, 12),  # 추석
    date(2022, 10, 3),  # 개천절
    date(2022, 10, 9),  # 한글날
    date(2022, 12, 25),  # 크리스마스
}

holidays_2023 = {
    date(2023, 1, 1),  # 새해
    date(2023, 1, 21), date(2023, 1, 22), date(2023, 1, 23), date(2023, 1, 24),  # 설
    date(2023, 3, 1),  # 삼일절
    date(2023, 5, 5),  # 어린이날
    date(2023, 5, 26),  # 석가탄신일
    date(2023, 6, 6),  # 현충일
    date(2023, 8, 15),  # 광복절
    date(2023, 9, 28), date(2023, 9, 29), date(2023, 9, 30),  # 추석
    date(2023, 10, 3),  # 개천절
    date(2023, 10, 9),  # 한글날
    date(2023, 12, 25),  # 크리스마스
}


def weekend(begin, end):
    weekends = set()

    current = begin
    while current <= end:
        if current.weekday() in [5, 6]:
            weekends.add(current)
        current += timedelta(days=1)

    return weekends

# weekends_2021 = weekend(2021)
# weekends_2022 = weekend(2022)

# leaves = set()  # later implement
# off_the_clock = set()  # later implement
# combat_closed = set()  # later implement
