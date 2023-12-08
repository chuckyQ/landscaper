import typing as t
from itertools import chain
import re
from flask import Blueprint, request, abort, jsonify
from collections import defaultdict

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import (User,
                             Job,
                             Crew,
                             Account,
                             SingleJob,
                             DailyJob,
                             WeeklyJob,
                             MonthlyJob,
                             YearlyJob,
                            )

from landfile.schema import schema
from landfile.schema.api import validate

jobs = Blueprint('jobs', 'jobs', url_prefix='/jobs')


def get_user():

    u: User = User.query.all()[0]

    if u is None:
        abort(500)

    assert isinstance(u, User)

    if not u.is_admin:
        abort(403)

    return u

def _get_jobs(account_id: int, start_date: str, end_date: str) -> t.Tuple[t.List[SingleJob], t.List[DailyJob],
                                                           t.List[WeeklyJob], t.List[MonthlyJob],
                                                           t.List[YearlyJob],
                                                           ]:
    def _get(cls):
        return cls.query.filter(cls.account_id==account_id,
                                # Remember, we are looking for overlap so
                                # recurring jobs may start before. Anything
                                # ending before the provided start date will
                                # not show on the calendar.
                                cls.canceled==False,
                                cls.start_date<=end_date,
                                cls.end_date>=start_date).all()

    _single_jobs: t.List[SingleJob] = _get(SingleJob)
    _daily_jobs: t.List[DailyJob] = _get(DailyJob)
    _weekly_jobs: t.List[WeeklyJob] = _get(WeeklyJob)
    _monthly_jobs: t.List[MonthlyJob] = _get(MonthlyJob)
    _yearly_jobs: t.List[YearlyJob] = _get(YearlyJob)

    return (_single_jobs, _daily_jobs,
            _weekly_jobs, _monthly_jobs,
            _yearly_jobs
    )


@jobs.route('', methods=['GET'])
# @jwt_required
def get_jobs():

    u = get_user()

    js = request.args
    date = js.get('date', None)
    if date is not None:
        jobs = Job.query.filter(Job.date == date).all()
        return jsonify([j.json() for j in jobs])

    start_date = js.get('startDate')
    end_date = js.get('endDate')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if start_date is None or end_date is None:
        abort(500)

    for dt in [start_date, end_date]:
        if not re.match('\d{4}-\d{2}-\d{2}', dt):
            abort(500)


    _jobs = defaultdict(list)

    for job in chain(*_get_jobs(account_id=u.account.id, start_date=start_date, end_date=end_date)):
        for date in job.gen_dates():
            _jobs[date].append(job.job_id)

    return _jobs


@validate(
  isRecurring=schema.Boolean(),
  recurringType=schema.String(),
  startDate=schema.String(),
  endDate=schema.String(),
  useEndDate=schema.Boolean(),
  recurrences=schema.Integer(),
  custID=schema.String(),
  crews=schema.Array(schema.String, minsize=1),
  notes=schema.String(),
)
def _create_daily_job(acc: Account, isRecurring: bool,
                      custID: str, notes: str, startDate: str,
                      endDate: str, useEndDate: bool,
                      recurringType: str, recurrences: int,
                      crews: t.List[str],
                      ):

    assert isRecurring
    assert recurringType == 'daily'

    crews_ = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews_.append(c)

    for c in crews_:

        if useEndDate:
            daily = acc.add_daily_job_end_date(notes=notes, start_date=startDate,
                                            end_date=endDate, cust_id=custID, crew_id=c.crew_id)
        else:
            daily = acc.add_daily_job_end_after(notes=notes, cust_id=custID,
                                                start_date=startDate, recurrences=recurrences,
                                                crew_id=c.crew_id)

    daily.save()


@validate(
  isRecurring=schema.Boolean(),
  recurringType=schema.String(),
  custID=schema.String(),
  notes=schema.String(),
  crews=schema.Array(schema.String, minsize=1),
  startDate=schema.String(),
  endDate=schema.String(),
  useEndDate=schema.Boolean(),
  recurrences=schema.Integer(),
  nWeeks=schema.Integer(),
  sunday=schema.Boolean(),
  monday=schema.Boolean(),
  tuesday=schema.Boolean(),
  wednesday=schema.Boolean(),
  thursday=schema.Boolean(),
  friday=schema.Boolean(),
  saturday=schema.Boolean(),
)
def _create_weekly_job(acc: Account, isRecurring: bool, recurringType: str,
                       custID: str, notes: str, crews: t.List[str],
                       startDate: str, endDate: str, useEndDate: bool, nWeeks: int,
                       recurrences: int, sunday: bool, monday: bool, tuesday: bool,
                       wednesday: bool, thursday: bool, friday: bool, saturday: bool):

    assert isRecurring
    assert recurringType == 'weekly'

    crews_: t.List[Crew] = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews_.append(c)

    for c in crews_:

        if useEndDate:
            weekly = acc.add_weekly_job_end_date(notes=notes, start_date=startDate,
                                                 end_date=endDate, cust_id=custID,
                                                 n_weeks=nWeeks, crew_id=c.id,
                                                 sunday=sunday,
                                                 monday=monday, tuesday=tuesday,
                                                 wednesday=wednesday, thursday=thursday,
                                                 friday=friday, saturday=saturday,
                                                 )

        else:
            weekly = acc.add_weekly_job_end_after(start_date=startDate, recurrences=recurrences,
                                                  n_weeks=nWeeks, cust_id=custID,
                                                  notes=notes, crew_id=c.crew_id, sunday=sunday,
                                                  monday=monday, tuesday=tuesday,
                                                  wednesday=wednesday, thursday=thursday,
                                                  friday=friday, saturday=saturday,
                                                  )

        weekly.save()


@validate(
    isRecurring=schema.Boolean(),
    recurringType=schema.String(),
    startDate=schema.Date(),
    endDate=schema.String(),
    useEndDate=schema.Boolean(),
    weekday=schema.Integer(),
    recurrences=schema.Integer(),
    day=schema.Integer(),
    custID=schema.String(),
    crews=schema.Array(schema.String, minsize=1),
    notes=schema.String(),
    isSpecificDay=schema.Boolean(),
    ordinal=schema.Integer(),
    nMonths=schema.Integer(),
)
def _create_monthly_job(acc: Account, isRecurring: bool, recurringType: str,
                        custID: str, notes: str, crews: t.List[str], startDate: str,
                        endDate: str, useEndDate: bool, nMonths: int,
                        isSpecificDay: bool, ordinal: int, weekday: int, day: int,
                        recurrences: int,
                        ):


    assert isRecurring
    assert recurringType == 'monthly'

    crews_: t.List[Crew] = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews_.append(c)

    for c in crews_:

        if useEndDate:
            # Day 1 of every 2 months
            monthly = acc.add_monthly_job_end_date(start_date=startDate, end_date=endDate,
                                                cust_id=custID, notes=notes, crew_id=c.crew_id,
                                                n_months=nMonths, use_specific_day=isSpecificDay,
                                                weekday=weekday, ordinal=ordinal, day=day,
                                                )

        else:
            # First Wednesday of every March
            monthly = acc.add_monthly_job_end_after(start_date=startDate, recurrences=recurrences,
                                                    notes=notes, cust_id=custID, ordinal=ordinal,
                                                    use_specific_day=isSpecificDay, n_months=nMonths,
                                                    day=day, weekday=weekday, crew_id=c.crew_id,
                                                    )

        monthly.save()

@validate(
    isRecurring=schema.Boolean(),
    recurringType=schema.String(),
    month=schema.Integer(),
    day=schema.Integer(),
    startDate=schema.Date(),
    endDate=schema.String(),
    recurrences=schema.Integer(),
    useEndDate=schema.Boolean(),
    custID=schema.String(),
    crews=schema.Array(schema.String, minsize=1),
    notes=schema.String(),
    ordinal=schema.Integer(),
    weekday=schema.Integer(),
)
def _create_yearly_job(acc: Account, isRecurring: bool, recurringType: str,
                       month: int, day: int, startDate: str, endDate: str,
                       recurrences: int, useEndDate: bool,
                       custID: str, crews: t.List[str], notes: str,
                       ordinal: int, weekday: int,
                       ):

    assert isRecurring
    assert recurringType == 'yearly'

    crews_: t.List[Crew] = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews_.append(c)

    for c in crews_:

        if useEndDate:
            yearly = acc.add_yearly_job_end_at(start_date=startDate, end_date=endDate,
                                      cust_id=custID, notes=notes, crew_id=c.crew_id,
                                      ordinal=ordinal, day=day, month=month, weekday=weekday,
                                      )
        else:
            yearly = acc.add_yearly_job_end_after(start_date=startDate, recurrences=recurrences,
                                         cust_id=custID, crew_id=c.crew_id, notes=notes,
                                         ordinal=ordinal, day=day, month=month,
                                         )
        yearly.save()


@validate(
    isRecurring=schema.Boolean(),
    recurringType=schema.String(),
    date=schema.Date(),
    custID=schema.String(),
    crews=schema.Array(schema.String, minsize=1),
    notes=schema.String(),
)
def _create_single_job(acc: Account, isRecurring: bool, recurringType: str,
                       date: str, custID: str, crews: t.List[str], notes: str):

    assert not isRecurring

    crews_ = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews_.append(c)

    for c in crews_:
        _ = acc.add_job(cust_id=custID, crew_id=crew_id, date=date, notes=notes)


@jobs.route('', methods=['POST'])
def create_job():

    u = get_user()

    if not u.is_admin:
        abort(403)

    acc = u.account

    js = request.json

    if not js.get('isRecurring', False):
        _create_single_job(acc=acc)
        return {}

    recurring_type = js.get('recurringType')
    if recurring_type == 'daily':
        _create_daily_job(acc=acc)
        return {}

    if recurring_type == 'weekly':
        _create_weekly_job(acc=acc)
        return {}

    if recurring_type == 'monthly':
        _create_monthly_job(acc=acc)
        return {}

    if recurring_type == 'yearly':
        _create_yearly_job(acc=acc)
        return {}

    abort(500)
