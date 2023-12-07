from datetime import datetime

from landfile import dateutil


def test_ordinal_date():

    dt = dateutil.get_ordinal_date(2023, dateutil.DECEMBER, dateutil.FIRST, dateutil.WEDNESDAY)
    assert dt == datetime(2023, dateutil.DECEMBER, 6)


def test_ordinal_date2():

    dt = dateutil.get_ordinal_date(2023, dateutil.DECEMBER, dateutil.LAST, dateutil.WEDNESDAY)
    assert dt == datetime(2023, dateutil.DECEMBER, 27)


def test_weekly_date():

    expected = [
        '2023-12-10',
        '2023-12-11',
        '2023-12-24',
        '2023-12-25',
    ]

    _dates = []
    for each in dateutil.gen_weekly_dates_end_date('2023-12-10',
                                                   '2023-12-26',
                                                   n_weeks=2,
                                                   sunday=True, monday=True):
        _dates.append(each)

    assert expected == _dates
