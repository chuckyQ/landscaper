import typing as t
from datetime import datetime, timedelta
from time import time
import string
import random

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from landfile import dateutil

db = SQLAlchemy()

crew_table = db.Table(
    'crew_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('crew_id', db.Integer, db.ForeignKey('crews.id')),
)

job_table = db.Table(
    'crew_jobs',
    db.Column('crew_id', db.Integer(), db.ForeignKey('crews.id')),
    db.Column('job_id', db.Integer(), db.ForeignKey('jobs.id')),
)

daily_jobs_jct = db.Table(
    'daily_jobs_junction',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('crew_id', db.Integer(), db.ForeignKey('crews.id')),
    db.Column('dailyjob_id', db.Integer, db.ForeignKey('daily_jobs.id')),
)

weekly_jobs_jct = db.Table(
    'weekly_jobs_junction',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('crew_id', db.Integer(), db.ForeignKey('crews.id')),
    db.Column('weeklyjob_id', db.Integer, db.ForeignKey('weekly_jobs.id')),
)

monthly_jobs_jct = db.Table(
    'monthly_jobs_junction',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('crew_id', db.Integer(), db.ForeignKey('crews.id')),
    db.Column('monthlyjob_id', db.Integer, db.ForeignKey('monthly_jobs.id')),
)

yearly_jobs_jct = db.Table(
    'yearly_jobs_junction',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('crew_id', db.Integer(), db.ForeignKey('crews.id')),
    db.Column('yearlyjob_id', db.Integer, db.ForeignKey('yearly_jobs.id')),
)

def gen_id(size=14, chars=string.ascii_letters + string.digits):
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.choice(chars) for _ in range(size))


class Account(db.Model):

    __tablename__ = 'accounts'

    id: int = db.Column(db.Integer, primary_key=True)
    acc_id: str = db.Column(db.String, index=True)
    email: str = db.Column(db.String, index=True, unique=True)

    customers: t.List['Customer']

    admins: t.List['User']
    members: t.List['User']
    jobs: t.List['Job']

    def __init__(self, email: str):

        self.email = email
        self.acc_id = 'acc_' + gen_id()


    def add_customer(self, address: str, contact_name: str, phone_number: str, notes: str):

        c = Customer(
            address=address,
            contact_name=contact_name,
            phone_number=phone_number,
            notes=notes,
            account_id=self.id,
        )

        c.save()
        return c


    def add_user(self, email: str, phone_number: str, password: str, is_admin: bool):

        u = User(
            password=password,
            email=email,
            account_id=self.id,
            is_admin=is_admin,
            phone_number=phone_number,
        )

        u.save()

        return u


    def add_crew(self, name: str, description: str):

        c = Crew(name=name, description=description, account_id=self.id)
        c.save()
        return c


    def add_job(self, cust_id: str, date_timestamp: float, notes: str):

        j = Job(cust_id=cust_id, account_id=self.id,
                notes=notes, work_date_timestamp=date_timestamp)
        j.save()
        return j


    def save(self):

        db.session.add(self)
        db.session.commit()


    def json(self):

        return {
            'username' : self.username,
            'plan' : self.plan,

        }


    def search_customer(self, search_term: str) -> t.List['Customer']:

        from sqlalchemy import func

        term = search_term.strip()

        if term == '':
            return []

        customers = Customer.query.filter(
                    func.lower(Customer.contact_name).contains(func.lower(term)),
                    ).all()

        return customers


    def add_daily_job_end_at(self, notes: str, start_date: str, end_date: str, cust_id: str):

        dj = DailyJob(
            cust_id=cust_id,
            start_date=start_date,
            end_date=end_date,
            end_after=-1,
            use_end_date=True,
            use_end_after=False,
            account_id=self.id,
            notes=notes,
        )

        dj.save()
        return dj


    def add_daily_job_end_after(self, notes: str, start_date: str, end_after: int, cust_id: str):


        dj = DailyJob(
            cust_id=cust_id,
            start_date=start_date,
            end_date='',
            end_after=end_after,
            use_end_date=False,
            use_end_after=True,
            account_id=self.id,
            notes=notes,
        )

        dj.save()
        return dj


    def add_weekly_job_end_date(self, notes: str, start_date: str, end_date: str,
                                 cust_id: str, n_weeks: int,
                                 sunday=False, monday=False, tuesday=False,
                                 wednesday=False, thursday=False, friday=False,
                                 saturday=False):

        wj = WeeklyJob(
            account_id=self.id,
            start_date=start_date,
            end_date=end_date,
            cust_id=cust_id,
            n_weeks=n_weeks,
            end_after=-1,
            use_end_after=False,
            use_end_date=True,
            notes=notes,
            sunday=sunday,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
        )

        wj.save()

        return wj


    def add_weekly_job_end_after(self, start_date: str, end_after: int, n_weeks: int,
                                    cust_id: str, notes: str,
                                    sunday=False, monday=False, tuesday=False,
                                    wednesday=False, thursday=False, friday=False,
                                    saturday=False,
                                    ):

        wj = WeeklyJob(
            start_date=start_date,
            end_date='',
            end_after=end_after,
            cust_id=cust_id,
            use_end_after=False,
            use_end_date=True,
            n_weeks=n_weeks,
            sunday=sunday,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            notes=notes,
        )

        wj.save()

        return wj


    def add_monthly_job_end_date(self, start_date: str, end_date: str,
                                  cust_id: str, notes: str, n_months: int,
                                  use_specific_day: bool, weekday: int, day: int):

        mj = MonthlyJob(
            notes=notes,
            cust_id=cust_id,
            n_months=n_months,
            start_date=start_date,
            end_date=end_date,
            use_end_after=False,
            use_end_date=True,
            use_specific_day=use_specific_day,
            weekday=weekday,
            day=day,
        )

        mj.save()


    def add_monthly_job_end_after(self, notes: str, start_date: str, end_after: int,
                                    cust_id: str, ordinal: int,
                                    day: int, use_specific_day: bool, month: int,
                                    weekday: int):

        mj = MonthlyJob(
            cust_id=cust_id,
            ordinal=ordinal,
            day=day,
            use_specific_day=use_specific_day,
            start_date=start_date,
            end_date='',
            end_after=end_after,
            use_end_after=True,
            use_end_at=False,
            weekday=weekday,
            month=month,
            notes=notes,
        )

        mj.save()


    def add_yearly_job_end_at(self, start_date: str, end_date: str,
                                cust_id: str, notes: str, crew_id: str,
                                ordinal: str, day: int, month: int, weekday: str,
                                ):

        yj = YearlyJob(
            account_id=self.id,
            cust_id=cust_id,
            notes=notes,
            crew_id=crew_id,
            start_date=start_date,
            end_after=-1,
            end_date=end_date,
            use_end_after=False,
            use_end_at=True,
            ordinal=ordinal,
            weekday=weekday,
            day=day,
            month=month,
        )

        yj.save()


    def add_yearly_job_end_after(self, notes: str, start_date: str, end_after: int,
                                cust_id: str, crew_id: str,
                                ordinal: str, day: int, month: int,
                                ):

        yj = YearlyJob(
            account_id=self.id,
            cust_id=cust_id,
            notes=notes,
            crew_id=crew_id,
            start_date=start_date,
            end_after=end_after,
            end_date='',
            use_end_after=False,
            use_end_at=True,
            ordinal=ordinal,
            day=day,
            month=month,
        )

        yj.save()


    def add_job(self, cust_id: str, date: str, crew_id: str, notes: str):

        j = Job(
            cust_id=cust_id,
            date=date,
            account_id=self.id,
            notes=notes,
            crew_id=crew_id,
        )

        j.save()

        return j


    def get_customer(self, cust_id: str):

        return Customer.query.filter(cust_id=cust_id,
                                     account_id=self.id).first()


    def get_job(self, job_id: str):

        return Job.query.filter(job_id=job_id,
                                account_id=self.id).first()


    def get_user(self, user_id: str):

        return User.query.filter(user_id=user_id,
                                 account_id=self.id).first()


class Customer(db.Model):

    __tablename__ = 'customers'

    id: int = db.Column(db.Integer, primary_key=True)
    cust_id: str = db.Column(db.String, unique=True)

    # An address is unique, but it could be used
    # across multiple accounts
    address: str = db.Column(db.String)
    contact_name: str = db.Column(db.String)
    phone_number: str = db.Column(db.String)
    notes: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    canceled: bool = db.Column(db.Boolean)
    account: Account = db.relationship('Account', backref='customers')


    def __init__(self, address: str, contact_name: str,
                 phone_number: str, notes: str, account_id: int):

        self.address = address
        self.cust_id = 'cus_' + gen_id()
        self.contact_name = contact_name
        self.notes = notes
        self.account_id = account_id
        self.phone_number = phone_number
        self.canceled = False


    def save(self):

        db.session.add(self)
        db.session.commit()


    def json(self):

        return {
            'custID' : self.cust_id,
            'name' : self.contact_name,
            'phoneNumber' : self.phone_number,
            'address' : self.address,
            'notes' : self.notes,
        }


class User(db.Model):

    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: str = db.Column(db.String, index=True)

    email: str = db.Column(db.String, unique=True)
    password: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    is_admin: bool = db.Column(db.Boolean)
    phone_number: str = db.Column(db.String)

    account: Account = db.relationship('Account', backref='members')
    crews: t.List['Crew']  = db.relationship('Crew', secondary=crew_table, back_populates='members')


    def __init__(self, email: str, password: str, phone_number: str, account_id: int, is_admin: bool):

        self.user_id = 'user_' + gen_id()
        self.password = generate_password_hash(password)
        self.email = email
        self.account_id = account_id
        self.is_admin = is_admin
        self.phone_number = phone_number


    def verify_password(self, password: str):

        return check_password_hash(self.password, password)


    def save(self):

        db.session.add(self)
        db.session.commit()


    def is_account_admin(self):

        return self in self.account.admins


    def json(self):

        return {
            'userID' : self.user_id,
            'email' : self.email,
            'phoneNumber' : self.phone_number,
        }


class Crew(db.Model):

    __tablename__ = 'crews'

    id: int = db.Column(db.Integer, primary_key=True)
    crew_id: str = db.Column(db.String, index=True)

    name: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    description: str = db.Column(db.String)
    deleted: bool = db.Column(db.Boolean)

    account: Account = db.relationship('Account', backref='crews')
    jobs: t.List['Job'] = db.relationship('Job', secondary=job_table, back_populates='crews')
    members: t.List['User'] = db.relationship('User', secondary=crew_table, back_populates='crews')

    daily_jobs: t.List['DailyJob'] = db.relationship('DailyJob', secondary=daily_jobs_jct, back_populates='crews')
    weekly_jobs: t.List['WeeklyJob'] = db.relationship('WeeklyJob', secondary=weekly_jobs_jct, back_populates='crews')
    monthly_jobs: t.List['MonthlyJob'] = db.relationship('MonthlyJob', secondary=monthly_jobs_jct, back_populates='crews')
    yearly_jobs: t.List['MonthlyJob'] = db.relationship('YearlyJob', secondary=yearly_jobs_jct, back_populates='crews')

    def __init__(self, name: str, description: str, account_id: int):

        self.name = name
        self.account_id = account_id
        self.description = description
        self.crew_id = 'crew_' + gen_id()
        self.deleted = False


    def save(self):

        db.session.add(self)
        db.session.commit()


    def json(self, get_jobs=False, get_members=False):

        if get_jobs:
            jobs = [job.json() for job in self.jobs]
        else:
            jobs = []

        if get_members:
            members = [u.json() for u in self.members]
        else:
            members = []

        return {
            'crewID' : self.crew_id,
            'name' : self.name,
            'description' : self.description,
            'members' : members,
            'jobs' : jobs,
        }


    def delete(self):

        self.deleted = True
        db.session.add(self)
        db.session.commit()


class Job(db.Model):

    __tablename__ = 'jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String, index=True)
    cust_id: str = db.Column(db.String)
    name: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    created_timestamp: float = db.Column(db.Float)
    last_updated_timestamp: float = db.Column(db.Float)
    address: str = db.Column(db.String)
    notes: str = db.Column(db.String)
    canceled: bool = db.Column(db.Boolean)
    date: str = db.Column(db.String)

    # Added by the Comment model
    comments: t.List['Comment']

    account = db.relationship('Account', backref='jobs')

    crews: t.List['Crew'] = db.relationship('Crew', secondary=job_table, back_populates='jobs')


    def __init__(self, cust_id: str, account_id: int, notes: str, date: str):

        self.account_id = account_id
        self.cust_id = cust_id
        now = time() * 1000 # Convert to milliseconds to make working with frontend easier
        self.created_timestamp = now
        self.last_updated_timestamp = now
        self.job_id = 'job_' + gen_id()
        self.date = date
        self.notes = notes


    def save(self):

        # We want milliseconds for the frontend
        self.last_updated_timestamp = time() * 1000

        db.session.add(self)
        db.session.commit()


    def json(self, get_crews=False, get_comments=False):

        if get_comments:
            comments = [c.json() for c in sorted(self.comments, key=lambda c: c.created_timestamp)]
        else:
            comments = []

        if get_crews:
            crews =  [c.json() for c in self.crews]
        else:
            crews = []

        return {
            'jobID' : self.job_id,
            'name' : self.name,
            'address' : self.address,
            'date' : self.date,
            'createdTimestamp' : self.created_timestamp,
            'lastUpdatedTimestamp' : self.last_updated_timestamp,
            'crews' : crews,
            'notes' : self.notes,
            'comments' : comments,
        }


    def add_comment(self, email: str, text: str):

        c = Comment(
            email=email,
            text=text,
            job_id=self.id,
        )

        c.save()

        return c


    def delete(self):

        self.canceled = True
        db.session.add(self)
        db.session.commit()


class DailyJob(db.Model):

    __tablename__ = 'daily_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.Integer)
    crew_id: str = db.Column(db.Integer)
    notes: str = db.Column(db.String)
    start_date: str = db.Column(db.String)
    end_date: str = db.Column(db.String)
    end_after: int = db.Column(db.Integer)
    use_end_date: bool = db.Column(db.Boolean)
    use_end_after: bool = db.Column(db.Boolean)
    canceled: bool = db.Column(db.Boolean)

    account: Account = db.relationship('Account', backref='daily_jobs')
    crews: t.List['Crew'] = db.relationship('Crew', secondary=daily_jobs_jct, back_populates='daily_jobs')

    def __init__(self, cust_id: int,
                 notes: str,
                 start_date: str,
                 end_after: int,
                 end_date: str,
                 use_end_date: bool,
                 use_end_after: bool,
                 account_id: int
                 ):

        self.job_id = f'dailyjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_date = start_date
        self.end_date = end_date
        self.end_after = end_after
        self.use_end_date = use_end_date
        self.use_end_after = use_end_after
        self.canceled = False
        self.account_id = account_id
        self.notes = notes


    def save(self):

        self.end_date = self.get_end_date()
        db.session.add(self)
        db.session.commit()


    def get_end_date(self):

        if self.use_end_date:
            return self.end_date

        dt = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = dt + timedelta(days=self.end_after)
        return end.strftime('%Y-%m-%d')


    def __repr__(self):

        return f'{self.__class__.__qualname__}(id={self.id}, ' \
               f'job_id={self.job_id!r}, ' \
               f'start_date={self.start_date!r}, ' \
               f'end_date={self.end_date!r}, ' \
               f'use_end_date={self.use_end_date}' \
               f')'


class WeeklyJob(db.Model):

    __tablename__ = 'weekly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.String)
    notes: str = db.Column(db.String)

    start_date: str = db.Column(db.String)

    end_date: str = db.Column(db.String)
    use_end_date: bool = db.Column(db.Boolean)

    end_after: int = db.Column(db.Integer)
    use_end_after: bool = db.Column(db.Boolean)

    n_weeks: int = db.Column(db.Integer)

    canceled: bool = db.Column(db.Boolean)

    sunday: bool = db.Column(db.Boolean)
    monday: bool = db.Column(db.Boolean)
    tuesday: bool = db.Column(db.Boolean)
    wednesday: bool = db.Column(db.Boolean)
    thursday: bool = db.Column(db.Boolean)
    friday: bool = db.Column(db.Boolean)
    saturday: bool = db.Column(db.Boolean)

    account: 'Account' = db.relationship('Account', backref='weekly_jobs')
    crews: t.List['Crew'] = db.relationship('Crew', secondary=weekly_jobs_jct, back_populates='weekly_jobs')

    def __init__(self, account_id: int, cust_id: str, notes: str, n_weeks: int,
                 sunday: bool, monday: bool,
                 tuesday: bool, wednesday: bool,
                 thursday: bool, friday: bool,
                 saturday: bool,
                 start_date: str,
                 end_date: str,
                 end_after: int,
                 use_end_date: bool,
                 use_end_after: bool,
                 ):

        self.job_id = f'weekjob_{gen_id(18)}'
        self.account_id = account_id

        self.cust_id = cust_id
        self.start_date = start_date
        self.end_date = end_date
        self.canceled = False
        self.end_after = end_after
        self.use_end_date = use_end_date
        self.use_end_after = use_end_after
        self.n_weeks = n_weeks
        self.notes = notes

        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday


    def delete(self):

        self.canceled = True
        db.session.add(self)
        db.session.commit()


    def save(self):

        self.end_date = self.get_end_date()

        db.session.add(self)
        db.session.commit()


    def get_end_date(self):

        if self.use_end_date:
            return self.end_date

        assert self.use_end_after

        if self.end_after == 1:
            # No actual recurrence
            return self.start_date

        i = None
        for each in self.get_job_dates():
            i = each

        assert i is not None

        return i


    def get_job_dates(self):

        if self.use_end_date:
            yield from dateutil.gen_weekly_dates_end_date(
                start_date=self.start_date,
                end_date=self.end_date,
                n_weeks=self.n_weeks,
                sunday=self.sunday, monday=self.monday,
                tuesday=self.tuesday, wednesday=self.wednesday,
                thursday=self.thursday, friday=self.friday,
                saturday=self.saturday,
            )
            return

        assert self.use_end_after

        yield from dateutil.gen_weekly_dates_end_after(
            start_date=self.start_date,
            end_after=self.end_after,
            n_weeks=self.n_weeks,
            sunday=self.sunday, monday=self.monday,
            tuesday=self.tuesday, wednesday=self.wednesday,
            thursday=self.thursday, friday=self.friday,
            saturday=self.saturday,
            )


    def __repr__(self):

        return f'{self.__class__.__qualname__}(id={self.id}, job_id={self.job_id!r}, ' \
               f'start_date={self.start_date!r}, ' \
               f'end_date={self.end_date!r}, ' \
               f'end_after={self.end_after}, ' \
               f'use_end_date={self.use_end_date}, ' \
               f'use_end_after={self.use_end_after}' \
               f')'

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


def _roll_months(year: int, month: int):

    if month <= 12:
        return year, month

    while month > 12:
        month -= 12
        year += 1

    return year, month


class MonthlyJob(db.Model):

    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    LAST = 5

    __tablename__ = 'monthly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.String)
    notes: str = db.Column(db.String)

    start_date: str = db.Column(db.String)
    end_date: str = db.Column(db.String)
    end_after: int = db.Column(db.Integer)
    canceled: bool = db.Column(db.Boolean)
    day: int = db.Column(db.Boolean)
    ordinal: int = db.Column(db.Boolean)
    use_specific_day: bool = db.Column(db.Boolean)
    weekday: int = db.Column(db.Integer)
    n_months: int = db.Column(db.Integer)

    use_end_date: bool = db.Column(db.Boolean)
    use_end_after: bool = db.Column(db.Boolean)

    account: Account = db.relationship('Account', backref='monthly_jobs')
    crews: t.List['Crew'] = db.relationship('Crew', secondary=monthly_jobs_jct, back_populates='monthly_jobs')

    def __init__(self, cust_id: int,
                 day: int,
                 use_end_date: bool,
                 use_end_after: bool,
                 start_date: str,
                 end_date: str,
                 ordinal: int,
                 use_specific_day: bool,
                 weekday: int,
                 n_months: int,
                 notes: str,
                 ):

        self.job_id = f'monthjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_date = start_date
        self.end_date = end_date
        self.use_end_after = use_end_after
        self.use_end_date = use_end_date
        self.canceled = False
        self.n_months = n_months
        self.notes = notes

        self.use_specific_day = use_specific_day
        self.ordinal = ordinal
        self.weekday = weekday
        self.day = day


    def save(self):

        db.session.add(self)
        db.session.commit()


    def get_end_date(self):

        if self.use_end_date:
            return self.end_date

        if self.use_specific_day:
            return self._get_date_from_specific_day()

        return self._get_end_date_from_ordinal()


    def _get_date_from_specific_day(self):

        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        start = datetime(start_date.year, start_date.month, start_date.day)
        n = self.end_after

        if start_date.day <= self.day:
            # We can include the start month
            # in this recurrence
            n -= 1

        month = start_date.month
        year = start.year
        date = datetime(year, month, self.day)
        for _ in range(n):

            if month > 12:
                month = 1
                year += 1
            else:
                month += 1

            if year % 4 == 0 and month == 2:
                # TODO: fix this for every 100 years
                # and 400 years :-)
                max_day = 29
            else:
                max_day = MAX_MONTH_DAYS[month]

            date = datetime(year, month, min(self.day, max_day))

        return date.strftime('%Y-%m-%d')


    def _get_end_date_from_ordinal(self):

        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        first_day = datetime(start_date.year, start_date.month, 1)

        weekday = (first_day.weekday() + 1) % 7
        while weekday != self.weekday:
            # Find the first instance of the specified weekday
            first_day += timedelta(days=1)
            weekday = (first_day.weekday() + 1) % 7

        if self.ordinal < self.LAST:
            # Multiply by ordinal to have exact
            # date of the specified ordinal
            first_occurrence = first_day + timedelta(weeks=(self.ordinal - 1))

        else:
            year, month = _roll_months(year, start_date.month + 1)
            new_start = datetime(year, month, 1)
            weekday = (new_start.weekday() + 1) % 7
            while weekday != self.weekday:
                new_start -= timedelta(days=1)
                weekday = (new_start.weekday() + 1) % 7

            first_occurrence = new_start

        total_months = self.n_months * self.end_after
        if first_occurrence < start_date:
            # We cannot include the current
            # month because the ordinal date is
            # before the start date
            total_months += 1

        total = start_date.month + total_months

        year, month = _roll_months(first_occurrence.year, total)
        end_timeframe = datetime(year, month, 1)

        weekday = (end_timeframe.weekday() + 1) % 7
        while self.weekday != weekday:
            end_timeframe += timedelta(days=1)
            weekday = (end_timeframe.weekday() + 1) % 7

        if self.ordinal < self.LAST:
            # Multiply by ordinal to have exact
            # date of the specified ordinal
            last_occurrence = end_timeframe + timedelta(weeks=(self.ordinal - 1))
            return last_occurrence.strftime('%Y-%m-%d')

        year, month = _roll_months(end_timeframe.year, end_timeframe.month + 1)
        end_date = datetime(year, month, 1)

        weekday = (end_date.weekday() + 1) % 7
        while weekday != self.weekday:
            end_date -= timedelta(days=1)
            weekday = (end_date.weekday() + 1) % 7

        return end_date.strftime('%Y-%m-%d')


    def get_jobs(self):

        ...


class YearlyJob(db.Model):

    _ORDINAL_TO_INT = {
        '' : 0,
        'first' : 1,
        'second' : 2,
        'third' : 3,
        'fourth' : 4,
        'last' : 5,
    }

    __tablename__ = 'yearly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.String)
    notes: str = db.Column(db.String)

    # Indices of months (0-Jan, 1-Feb, etc...)
    month: int = db.Column(db.Integer)

    start_date: str = db.Column(db.String)

    end_date: str = db.Column(db.String)
    use_end_date: bool = db.Column(db.Boolean)

    end_after: int = db.Column(db.Integer)
    use_end_after: bool = db.Column(db.Boolean)

    use_specific_date: bool = db.Column(db.Boolean)
    month: int = db.Column(db.Integer)
    ordinal: int = db.Column(db.Integer)
    day: int = db.Column(db.Integer)
    canceled: bool = db.Column(db.Boolean)

    account: Account = db.relationship('Account', backref='yearly_jobs')
    crews: t.List['Crew'] = db.relationship('Crew', secondary=yearly_jobs_jct, back_populates='yearly_jobs')

    def __init__(self, account_id: int, cust_id: int, notes: str,
                 start_date: str, end_date: str, month: int, day: int,
                 end_after: int,  use_end_at: bool,
                 use_end_after: bool, ordinal: str, weekday: int,
                 ):

        self.account_id = account_id
        self.job_id = f'yearjob_{gen_id(18)}'
        self.cust_id = cust_id
        self.notes = notes
        self.start_date = start_date
        self.end_date = end_date
        self.end_after = end_after
        self.use_end_after = use_end_after
        self.use_end_at = use_end_at
        self.canceled = False
        self.ordinal = self._ORDINAL_TO_INT.get(ordinal, 0)
        self.month = month
        self.day = day
        self.weekday = weekday


    def save(self):

        db.session.add(self)
        db.session.commit()


class Comment(db.Model):

    __tablename__ = 'job_comments'

    id: int = db.Column(db.Integer, primary_key=True)
    job_comment_id: str = db.Column(db.String, index=True)

    email: str = db.Column(db.String)
    job_id: int = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    text: str = db.Column(db.String)
    created_timestamp: float = db.Column(db.Float)

    job: Job = db.relationship('Job', backref='comments')

    def __init__(self, email: str, text: str, job_id: int):

        self.email = email
        self.text = text
        self.job_id = job_id
        # We want to use milliseconds for the timestamp
        self.created_timestamp = time() * 1000


    def save(self):

        db.session.add(self)
        db.session.commit()


    def json(self):

        return {
            'email' : self.email,
            'timestamp' : self.created_timestamp,
            'text' : self.text,
        }


    def delete(self):

        db.session.delete(self)
        db.session.commit()


class Image(db.Model):

    __tablename__ = 'images'

    id: int = db.Column(db.Integer, primary_key=True)
    image_id: str = db.Column(db.String)
    job_id: str = db.Column(db.String, db.ForeignKey('jobs.job_id'))
    job: Job = db.relationship('Job', backref='images')

    # Timestamp (in milliseconds) when the image was created
    # The frontend expectes milliseconds for timestamps
    timestamp: float = db.Column(db.Float)


    def __init__(self, job_id: str, timestamp: float):

        self.job_id = job_id
        self.timestamp = timestamp
        self.image_id = 'img_' + gen_id()


    def save(self):

        db.session.add(self)
        db.session.commit()


    def delete(self):

        db.session.delete(self)
        db.session.commit()


class CancelMarker(db.Model):
    """This model is for holding dates for a recurring
    job that have been canceled.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: int = db.Column(db.String)
    date: str = db.Column(db.String)

    def __init__(self, job_id: str, date: str):

        self.job_id = job_id
        self.date = date


    def save(self):

        db.session.add(self)
        db.session.commit()


def create_account(email: str, password: str):

    a = Account(email=email)
    a.save()
    a.add_user(email=email, phone_number='', password=password, is_admin=True)
    return a
