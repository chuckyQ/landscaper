"""
This module contains functions for calcuating end dates with
ordinal information (first Sunday, last Tuesday) and dates that
have skip times (every 2 weeks, every 3 weeks, etc.)
"""

from datetime import date, timedelta, datetime

FIRST = 0
SECOND = 1
THIRD = 2
FOURTH = 3
LAST = 5

SUNDAY = 0
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6

WEEKDAYS = {
    SUNDAY,
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
}

ORDINALS = {
    FIRST,
    SECOND,
    THIRD,
    FOURTH,
    LAST,
}

JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 1
DECEMBER = 12

MONTHS = {
    JANUARY,
    FEBRUARY,
    MARCH,
    APRIL,
    MAY,
    JUNE,
    JULY,
    AUGUST,
    SEPTEMBER,
    OCTOBER,
    NOVEMBER,
    DECEMBER,
}

# Month indices to max days
MAX_MONTH_DAYS = {
    1 : 31,
    2 : 28, # Not counting leap years
    3 : 31,
    4 : 30,
    5 : 31,
    6 : 30,
    7 : 31,
    8 : 31,
    9 : 30,
    10 : 31,
    11 : 30,
    12 : 31,
}


def get_ordinal_date(year: int, month: int, ordinal: int, weekday: int):
    """Function for calculating dates based on ordinals
    (first, second, third, fourth, and last)

    >>> get_ordinal_date(2024, NOVEMBER, FIRST, SUNDAY)
    """
    if weekday not in WEEKDAYS:
        raise ValueError(f'Invalid weekday {weekday!r}')

    if ordinal not in ORDINALS:
        raise ValueError(f'invalid ordinal {ordinal}')

    if month not in MONTHS:
        raise ValueError(f'Invalid month {month!r}')

    if ordinal == LAST:
        return get_last_ordinal_date(year, month, weekday)

    start_date = datetime(year, month, 1)
    day = start_date.weekday()
    day = (day + 1) % 7
    n = 0
    while day != weekday:
        day = (day + 1) % 7
        n += 1

    if n == 0 and ordinal == FIRST:
        return start_date

    if n > 0:
        start_date += timedelta(days=n)

    if ordinal == FIRST:
        return start_date

    return start_date + timedelta(days=7*ordinal)


def get_last_ordinal_date(year: int, month: int, weekday: int):

    month += 1
    if month > 12:
        years, month = divmod(month, 12)
        year += years

    next_start = date(year, month, 1)

    day = (next_start.weekday() + 1) % 7
    delta = timedelta(days=1)
    while day != weekday:
        next_start -= delta
        day = (next_start.weekday() + 1) % 7

    return next_start


def get_latest_weekly_date_end_date(
                     start_date: str,
                     end_date: str,
                     n_weeks: int,
                     latest_day: int,
                     ):
    """
    Calculate the latest weekly date provided a start
    date and end date, the number of skip weeks (every
    2 weeks, every 3 weeks, etc.)
    and the latest weekday.

    >>> get_latest_weekly_date_end_date('2023-01-01',
                                        '2023-02-11',
                                        n_weeks=2,
                                        latest_day=TUESDAY),
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    next_week = start
    delta = timedelta(weeks=n_weeks)
    while next_week + delta < end:
        next_week += delta

    day = (next_week.weekday() + 1) % 7
    while day != latest_day:
        next_week -= timedelta(days=1)
        day = (next_week.weekday() + 1) % 7

    return next_week


def gen_daily_dates_end_date(start_date: str, end_date: str):

    if start_date > end_date:
        raise ValueError(f'Start date {start_date!r} cannot be '
                         f'greater than end date {end_date!r}.')

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    yield start_date

    delta = timedelta(days=1)
    while start < end:
        start += delta
        yield start.strftime('%Y-%m-%d')


def gen_daily_dates_end_after(start_date: str, end_after: int):

    if end_after < 1:
        raise ValueError("'end_after' must be >= 1.")

    start = datetime.strptime(start_date, '%Y-%m-%d')

    n = 0
    delta = timedelta(days=1)
    while n < end_after:
        start += delta
        n += 1
        yield start.strftime('%Y-%m-%d')


def gen_weekly_dates(start_date: str, n_weeks: int,
                      sunday=False, monday=False,
                      tuesday=False, wednesday=False,
                      thursday=False, friday=False,
                      saturday=False,
                      ):
    """This function is an infinite generator of dates based
    on a weekly recursion. It is up to the caller to
    determine an adequate number of iterations before stopping.
    """
    weekdays = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]

    if weekdays.count(True) == 0:
        raise ValueError('No weekday has been selected.')

    start = datetime.strptime(start_date, '%Y-%m-%d')

    weekday = (start.weekday() + 1) % 7
    first_week = [start + timedelta(days=x) for x in range(7)]

    # Swap weekday values to align with the previous date array
    selected = weekdays[weekday:] + weekdays[:weekday]

    n = 0
    while True:
        for s, day in zip(selected, first_week):
            if n == 0 and s:
                yield day.strftime('%Y-%m-%d')
                continue

            if s:
                d = day + timedelta(weeks=n * n_weeks)
                yield d.strftime('%Y-%m-%d')

        n += 1


def gen_weekly_dates_end_date(start_date: str, end_date: str, n_weeks: int,
                              sunday=False, monday=False,
                              tuesday=False, wednesday=False,
                              thursday=False, friday=False,
                              saturday=False,
                              ):

    if end_date < start_date:
        raise ValueError(f'Start date {start_date!r} cannot be '
                         f'greater than end date {end_date!r}.')

    if n_weeks < 1:
        raise ValueError(f'n_weeks {n_weeks} must be >= 1.')

    _ = datetime.strptime(end_date, '%Y-%m-%d') # Just verification

    for d in gen_weekly_dates(start_date=start_date, n_weeks=n_weeks,
                               sunday=sunday, monday=monday,
                               tuesday=tuesday, wednesday=wednesday,
                               thursday=thursday, friday=friday,
                               saturday=saturday):

        if d > end_date:
            break

        yield d


def gen_weekly_dates_end_after(start_date: str, end_after: int, n_weeks: int,
                               sunday=False, monday=False,
                               tuesday=False, wednesday=False,
                               thursday=False, friday=False,
                               saturday=False,
                               ):

    if end_after < 1:
        raise ValueError("'end_after' must be >= 1.")

    n = 0

    for d in gen_weekly_dates(start_date=start_date, n_weeks=n_weeks,
                               sunday=sunday, monday=monday,
                               tuesday=tuesday, wednesday=wednesday,
                               thursday=thursday, friday=friday,
                               saturday=saturday,
                               ):
        yield d
        n += 1

        if n == end_after:
            break


def gen_monthly_ordinal_dates(start_date: str, end_date: str, ordinal: int, day: int):

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    if end < start:
        raise ValueError('End date cannot be before start date.')

    year = start.year
    month = start.month
    dt = get_ordinal_date(year, month, ordinal, day)
    while True:

        if dt < start:
            month += 1
            if month > 12:
                month = 1
                year += 1
            dt = get_ordinal_date(year, month, day)
            continue

        yield dt.strftime('%Y-%m-%d')
        dt = get_ordinal_date(year, month, day)

        if dt > end:
            break

        month += 1
        if month > 12:
            month = 1
            year += 1


def gen_monthly_day_dates(start_date: str, end_date: str, day: int):
    """
    Generate a series of dates for a specific day
    >>> for each in gen_monthly_day_dates('2023-12-06', '2024-02-06', day=12): # doctest: +SKIP
    ...     print(each) # Prints '2023-12-12', '2024-01-12', '2024-02-12'
    """

    def _max_day(yr: int, mn: int, d: int):

        if mn == 2 and yr % 4 == 0:
            # TODO: fix this for 100 years and 400 years :-P
            return min(d, 29)

        return min(d, MAX_MONTH_DAYS[mn])

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    if end < start:
        raise ValueError('End date cannot be before start date.')

    year = start.year
    month = start.month

    dt = datetime(year, month, day)
    while True:

        if dt < start:
            month += 1
            if month > 12:
                month = 1
                year += 1
            dt = date(year, month, _max_day(year, month, day))
            continue

        yield dt.strftime('%Y-%m-%d')

        month += 1
        if month > 12:
            month = 1
            year += 1
        dt = datetime(year, month, _max_day(year, month, day))

        if dt > end:
            break
