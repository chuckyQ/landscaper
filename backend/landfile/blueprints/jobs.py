import typing as t
from flask import Blueprint, request, abort, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User, Job, Crew, Account
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
    if start_date is not None and end_date is not None:
        jobs = Job.query.filter(Job.date >= start_date, Job.date <= end_date).all()
        return jsonify([j.json() for j in jobs])

    return jsonify([j.json() for j in u.account.jobs])

@validate(
  isRecurring=schema.Boolean(),
  recurringType=schema.String(),
  startDate=schema.String(),
  endDate=schema.String(),
  useEndDate=schema.Boolean(),
  endAfter=schema.Integer(),
  custID=schema.String(),
  crews=schema.Array(schema.String, minsize=1),
  notes=schema.String(),
)
def _create_daily_job(acc: Account, isRecurring: bool,
                      custID: str, notes: str, startDate: str,
                      endDate: str, useEndDate: bool,
                      recurringType: str, endAfter: int,
                      crews: t.List[str],
                      ):

    assert isRecurring
    assert recurringType == 'daily'

    # print(request.json)
    # return {}

    if useEndDate:
        daily = acc.add_daily_job_end_at(notes=notes, start_date=startDate,
                                         end_date=endDate, cust_id=custID)
    else:
        daily = acc.add_daily_job_end_after(notes=notes, cust_id=custID,
                                            start_date=startDate, end_after=endAfter)

    crews = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews.append(c)

    daily.crews.extend(crews)
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
  endAfter=schema.Integer(),
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
                       endAfter: int, sunday: bool, monday: bool, tuesday: bool,
                       wednesday: bool, thursday: bool, friday: bool, saturday: bool):

    assert isRecurring
    assert recurringType == 'weekly'

    if useEndDate:
        weekly = acc.add_weekly_job_end_date(notes=notes, start_date=startDate, end_date=endDate,
                                          cust_id=custID, n_weeks=nWeeks,
                                          sunday=sunday, monday=monday, tuesday=tuesday,
                                          wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday,
                                          )

    else:
        weekly = acc.add_weekly_job_end_after(start_date=startDate, end_after=endAfter, n_weeks=nWeeks,
                                             cust_id=custID, notes=notes, sunday=sunday, monday=monday,
                                             tuesday=tuesday, wednesday=wednesday, thursday=thursday,
                                             friday=friday, saturday=saturday)

    crews = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews.append(c)

    weekly.crews.extend(crews)
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
                        endDate: str, useEndDate: str, nMonths: int,
                        isSpecificDay: bool, ordinal: int, weekday: int, day: int,
                        recurrences: int,
                        ):


    assert isRecurring
    assert recurringType == 'monthly'

    if useEndDate:
        # Day 1 of every 2 months
        monthly = acc.add_monthly_job_end_date(start_date=startDate, end_date=endDate,
                                               cust_id=custID, notes=notes,
                                               n_months=nMonths, use_specific_day=isSpecificDay,
                                               weekday=weekday, ordinal=ordinal, day=day,
                                               )

    else:
        monthly = acc.add_monthly_job_end_after(start_date=startDate, end_after=recurrences,
                                                notes=notes, cust_id=custID, ordinal=ordinal,
                                                use_specific_day=isSpecificDay, n_months=nMonths,
                                                day=day, weekday=weekday,
                                                )

    crews_ = []
    for crew_id in crews:
        c: Crew = Crew.query.filter(Crew.crew_id == crew_id, Crew.account_id == acc.id).first()
        if c is None:
            abort(500)
        crews_.append(c)

    monthly.crews.extend(crews_)
    monthly.save()


def _create_yearly_job(acc: Account, cust_id: str, notes: str):
    ...


def _create_single_job(acc: Account, cust_id: str, notes: str):
    ...

@jobs.route('', methods=['POST'])
def create_job():

    u = get_user()

    if not u.is_admin:
        abort(403)

    acc = u.account

    js = request.json

    if not js.get('isRecurring', False):
        _create_single_job(acc=acc,
                           cust_id=js['custID'],
                           name=js['name'],
                           address=js['address'],
                           )
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

    return {}
