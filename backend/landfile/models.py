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


    def add_crew(self, name: str, description: str, color: str, use_black_text: bool):

        c = Crew(name=name, description=description, account_id=self.id,
                 color=color, use_black_text=use_black_text)
        c.save()
        return c


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


    def add_daily_job_end_date(self, notes: str, start_date: str, end_date: str, cust_id: str, crew_id: str):

        dj = DailyJob(
            cust_id=cust_id,
            start_date=start_date,
            end_date=end_date,
            recurrences=-1,
            use_end_date=True,
            account_id=self.id,
            notes=notes,
            crew_id=crew_id,
        )

        dj.save()
        return dj


    def add_daily_job_end_after(self, notes: str, start_date: str, recurrences: int, cust_id: str, crew_id: str):


        dj = DailyJob(
            cust_id=cust_id,
            start_date=start_date,
            end_date='',
            recurrences=recurrences,
            use_end_date=False,
            account_id=self.id,
            notes=notes,
            crew_id=crew_id,
        )

        dj.save()
        return dj


    def add_weekly_job_end_date(self, notes: str, start_date: str, end_date: str,
                                 cust_id: str, n_weeks: int, crew_id: str,
                                 sunday=False, monday=False, tuesday=False,
                                 wednesday=False, thursday=False, friday=False,
                                 saturday=False):

        wj = WeeklyJob(
            account_id=self.id,
            start_date=start_date,
            end_date=end_date,
            cust_id=cust_id,
            n_weeks=n_weeks,
            recurrences=-1,
            use_end_date=True,
            notes=notes,
            crew_id=crew_id,
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


    def add_weekly_job_end_after(self, start_date: str, recurrences: int, n_weeks: int,
                                    cust_id: str, notes: str, crew_id: str,
                                    sunday=False, monday=False, tuesday=False,
                                    wednesday=False, thursday=False, friday=False,
                                    saturday=False,
                                    ):

        wj = WeeklyJob(
            account_id=self.id,
            start_date=start_date,
            end_date='',
            recurrences=recurrences,
            cust_id=cust_id,
            use_end_date=True,
            n_weeks=n_weeks,
            crew_id=crew_id,
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
                                  use_specific_day: bool, weekday: int, day: int,
                                  ordinal: int, crew_id: str,
                                  ):

        mj = MonthlyJob(
            notes=notes,
            cust_id=cust_id,
            n_months=n_months,
            start_date=start_date,
            end_date=end_date,
            use_end_date=True,
            recurrences=-1,
            use_specific_day=use_specific_day,
            weekday=weekday,
            day=day,
            ordinal=ordinal,
            crew_id=crew_id,
        )

        mj.save()

        return mj


    def add_monthly_job_end_after(self, notes: str, start_date: str, recurrences: int,
                                    cust_id: str, ordinal: int, day: int, n_months: int,
                                    use_specific_day: bool, weekday: int, crew_id: str):

        mj = MonthlyJob(
            cust_id=cust_id,
            ordinal=ordinal,
            day=day,
            use_specific_day=use_specific_day,
            start_date=start_date,
            end_date='',
            n_months=n_months,
            recurrences=recurrences,
            use_end_date=False,
            weekday=weekday,
            notes=notes,
            crew_id=crew_id,
        )

        mj.save()

        return mj


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
            recurrences=-1,
            end_date=end_date,
            use_end_date=True,
            ordinal=ordinal,
            weekday=weekday,
            day=day,
            month=month,
        )

        yj.save()

        return yj


    def add_yearly_job_end_after(self, notes: str, start_date: str, recurrences: int,
                                cust_id: str, crew_id: str,
                                ordinal: str, day: int, month: int,
                                ):

        yj = YearlyJob(
            account_id=self.id,
            cust_id=cust_id,
            notes=notes,
            crew_id=crew_id,
            start_date=start_date,
            recurrences=recurrences,
            end_date='',
            use_end_date=False,
            ordinal=ordinal,
            day=day,
            month=month,
        )

        yj.save()

        return yj


    def add_job(self, cust_id: str, date: str, crew_id: str, notes: str):

        j = SingleJob(account_id=self.id,
                      cust_id=cust_id,
                      crew_id=crew_id,
                      date=date,
                      notes=notes,
                      )

        j.save()

        return j


    def get_customer(self, cust_id: str) -> 'Customer':

        return Customer.query.filter(Customer.cust_id==cust_id,
                                     Customer.account_id==self.id).first()


    def get_job(self, job_id: str):

        return Job.query.filter(job_id=job_id,
                                account_id=self.id).first()


    def get_user(self, email: str) -> 'User':

        return User.query.filter(email=email,
                                 account_id=self.id).first()


    def get_crew(self, crew_id: str) -> 'Crew':

        return Crew.query.filter(Crew.crew_id == crew_id,
                                 Crew.account_id == self.id).first()


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
    color: str = db.Column(db.String)
    use_black_text: bool = db.Column(db.Boolean)

    account: Account = db.relationship('Account', backref='crews')
    members: t.List['User'] = db.relationship('User', secondary=crew_table, back_populates='crews')

    daily_jobs: t.List['DailyJob']
    weekly_jobs: t.List['WeeklyJob']
    monthly_jobs: t.List['MonthlyJob']
    yearly_jobs: t.List['MonthlyJob']

    def __init__(self, name: str, description: str, account_id: int, color: str, use_black_text: bool):

        self.name = name
        self.account_id = account_id
        self.description = description
        self.crew_id = 'crew_' + gen_id()
        self.deleted = False
        self.color = color
        self.use_black_text = use_black_text


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
            'color' : self.color,
            'useBlackText' : self.use_black_text,
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

    created_timestamp: float = db.Column(db.Float)
    last_updated_timestamp: float = db.Column(db.Float)
    address: str = db.Column(db.String)
    notes: str = db.Column(db.String)
    canceled: bool = db.Column(db.Boolean)
    date: str = db.Column(db.String)

    # Added by the Comment model
    comments: t.List['Comment']

    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account = db.relationship('Account', backref='jobs')

    crew_id: int = db.Column(db.Integer, db.ForeignKey('crews.id'))
    crew: Crew = db.relationship('Crew', backref='jobs')


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


class SingleJob(db.Model):

    __tablename__ = 'single_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.Integer)
    crew_id: str = db.Column(db.Integer)
    notes: str = db.Column(db.String)

    # These are always equal, but we want to keep
    # symmetry between all different types of jobs.
    start_date: str = db.Column(db.String)
    end_date: str = db.Column(db.String)

    canceled: bool = db.Column(db.Boolean)

    def __init__(self, account_id: int, cust_id: str,
                 crew_id: str, notes: str, date: str):

        self.job_id = f'sing_{gen_id()}'
        self.account_id = account_id
        self.cust_id = cust_id
        self.crew_id = crew_id
        self.notes = notes
        self.start_date = date
        self.end_date = date
        self.canceled = False


    def save(self):

        db.session.add(self)
        db.session.commit()


    def gen_dates(self):

        return [self.start_date]


    def json(self):

        return {
            'id' : self.job_id,
            'custID' : self.cust_id,
            'crewID' : self.crew_id,
        }


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
    recurrences: int = db.Column(db.Integer)
    use_end_date: bool = db.Column(db.Boolean)
    canceled: bool = db.Column(db.Boolean)

    crew_id: str = db.Column(db.String, db.ForeignKey('crews.crew_id'))

    account: Account = db.relationship('Account', backref='daily_jobs')
    crew: Crew = db.relationship('Crew', backref='daily_jobs')

    def __init__(self, cust_id: int,
                 notes: str,
                 start_date: str,
                 recurrences: int,
                 end_date: str,
                 use_end_date: bool,
                 account_id: int,
                 crew_id: str,
                 ):

        self.job_id = f'dailyjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_date = start_date
        self.end_date = end_date
        self.recurrences = recurrences
        self.use_end_date = use_end_date
        self.canceled = False
        self.account_id = account_id
        self.notes = notes
        self.crew_id = crew_id


    def save(self):

        self.end_date = self.get_end_date()
        db.session.add(self)
        db.session.commit()


    def get_end_date(self):

        if self.use_end_date:
            return self.end_date

        dt = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = dt + timedelta(days=self.recurrences)
        return end.strftime('%Y-%m-%d')


    def __repr__(self):

        return f'{self.__class__.__qualname__}(id={self.id}, ' \
               f'job_id={self.job_id!r}, ' \
               f'start_date={self.start_date!r}, ' \
               f'end_date={self.end_date!r}, ' \
               f'use_end_date={self.use_end_date}' \
               f')'


    def use_end_after(self):
        return not self.use_end_date


    def gen_dates(self):

        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')

        start = start_date
        while start <= end_date:
            yield start.strftime('%Y-%m-%d')
            start += timedelta(days=1)


    def json(self):

        return {
            'id' : self.job_id,
            'custID' : self.cust_id,
            'crewID' : self.crew_id,
        }

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
    recurrences: int = db.Column(db.Integer)
    n_weeks: int = db.Column(db.Integer)
    canceled: bool = db.Column(db.Boolean)

    sunday: bool = db.Column(db.Boolean)
    monday: bool = db.Column(db.Boolean)
    tuesday: bool = db.Column(db.Boolean)
    wednesday: bool = db.Column(db.Boolean)
    thursday: bool = db.Column(db.Boolean)
    friday: bool = db.Column(db.Boolean)
    saturday: bool = db.Column(db.Boolean)

    crew_id: str = db.Column(db.Integer, db.ForeignKey('crews.id'))

    account: 'Account' = db.relationship('Account', backref='weekly_jobs')
    crew: Crew = db.relationship('Crew', backref='weekly_jobs')

    def __init__(self, account_id: int, cust_id: str, notes: str, n_weeks: int,
                 sunday: bool, monday: bool,
                 tuesday: bool, wednesday: bool,
                 thursday: bool, friday: bool,
                 saturday: bool,
                 start_date: str,
                 end_date: str,
                 recurrences: int,
                 use_end_date: bool,
                 crew_id: str,
                 ):

        self.job_id = f'weekjob_{gen_id(18)}'
        self.account_id = account_id

        self.cust_id = cust_id
        self.start_date = start_date
        self.end_date = end_date
        self.canceled = False
        self.recurrences = recurrences
        self.use_end_date = use_end_date
        self.n_weeks = n_weeks
        self.notes = notes

        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.crew_id = crew_id


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

        if self.recurrences == 1:
            # No actual recurrence
            return self.start_date

        gen = dateutil.gen_weekly_dates(self.start_date, self.n_weeks,
                                        sunday=self.sunday, monday=self.monday,
                                        tuesday=self.tuesday, wednesday=self.wednesday,
                                        thursday=self.thursday, friday=self.friday,
                                        saturday=self.saturday)

        for i, each in enumerate(gen, start=1):
            if i > self.recurrences:
                break
            dt = each

        return dt


    def gen_dates(self):

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
            end_after=self.recurrences,
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
               f'recurrences={self.recurrences}, ' \
               f'use_end_date={self.use_end_date}' \
               f')'

    @property
    def use_end_after(self):
        return not self.use_end_date


    def json(self):

        return {
            'id' : self.job_id,
            'custID' : self.cust_id,
            'crewID' : self.crew_id,
        }


class MonthlyJob(db.Model):

    __tablename__ = 'monthly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.String)
    notes: str = db.Column(db.String)

    start_date: str = db.Column(db.String)
    end_date: str = db.Column(db.String)
    recurrences: int = db.Column(db.Integer)
    canceled: bool = db.Column(db.Boolean)
    day: int = db.Column(db.Boolean)
    ordinal: int = db.Column(db.Integer)
    use_specific_day: bool = db.Column(db.Boolean)
    weekday: int = db.Column(db.Integer)
    n_months: int = db.Column(db.Integer)

    use_end_date: bool = db.Column(db.Boolean)

    crew_id: str = db.Column(db.Integer, db.ForeignKey('crews.id'))

    account: Account = db.relationship('Account', backref='monthly_jobs')
    crew: Crew = db.relationship('Crew', backref='monthly_jobs')

    def __init__(self, cust_id: int,
                 day: int,
                 use_end_date: bool,
                 start_date: str,
                 end_date: str,
                 recurrences: int,
                 ordinal: int,
                 use_specific_day: bool,
                 weekday: int,
                 n_months: int,
                 notes: str,
                 crew_id: str,
                 ):

        self.job_id = f'monthjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_date = start_date
        self.end_date = end_date
        self.use_end_date = use_end_date
        self.recurrences = recurrences
        self.canceled = False
        self.n_months = n_months
        self.notes = notes

        self.use_specific_day = use_specific_day
        self.ordinal = ordinal
        self.weekday = weekday
        self.day = day
        self.crew_id = crew_id


    def save(self):

        db.session.add(self)
        db.session.commit()


    def get_end_date(self):

        if self.use_end_date:
            return self.end_date

        gen = dateutil.gen_monthly_ordinal_dates(self.start_date, self.end_date, self.ordinal, self.day)
        dt = next(gen)
        for each in gen:
            dt = each

        return dt


    def gen_dates(self):

        yield from dateutil.gen_monthly_ordinal_dates(self.start_date, self.end_date,
                                                      self.ordinal, self.weekday)


    def json(self):

        return {
            'id' : self.job_id,
            'custID' : self.cust_id,
            'crewID' : self.crew_id,
        }


class YearlyJob(db.Model):

    __tablename__ = 'yearly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    job_id: str = db.Column(db.String)
    cust_id: str = db.Column(db.String)
    notes: str = db.Column(db.String)

    month: int = db.Column(db.Integer)

    start_date: str = db.Column(db.String)

    end_date: str = db.Column(db.String)
    use_end_date: bool = db.Column(db.Boolean)
    recurrences: int = db.Column(db.Integer)

    use_specific_date: bool = db.Column(db.Boolean)
    month: int = db.Column(db.Integer)
    ordinal: int = db.Column(db.Integer)
    day: int = db.Column(db.Integer)
    canceled: bool = db.Column(db.Boolean)

    crew_id: str = db.Column(db.String, db.ForeignKey('crews.crew_id'))
    weekday: int = db.Column(db.Integer)

    account: Account = db.relationship('Account', backref='yearly_jobs')
    crew: Crew = db.relationship('Crew', backref='yearly_jobs')

    def __init__(self, account_id: int, cust_id: int, notes: str,
                 start_date: str, end_date: str, month: int, day: int,
                 recurrences: int,  use_end_date: bool, ordinal: int,
                 weekday: int, crew_id: str,
                 ):

        self.account_id = account_id
        self.job_id = f'yearjob_{gen_id(18)}'
        self.cust_id = cust_id
        self.notes = notes
        self.start_date = start_date
        self.end_date = end_date
        self.recurrences = recurrences
        self.use_end_date = use_end_date
        self.canceled = False
        self.ordinal = ordinal
        self.month = month
        self.day = day
        self.weekday = weekday
        self.crew_id = crew_id


    def save(self):

        db.session.add(self)
        db.session.commit()

    @property
    def use_end_after(self):
        return not self.use_end_date


    def gen_dates(self):

        if self.use_specific_date:
            yield from dateutil.gen_yearly_dates_day(self.start_date, self.end_date,
                                                     self.month, self.day)
            return

        yield from dateutil.gen_yearly_dates_ordinal(self.start_date, self.end_date,
                                                     self.month + 1, self.ordinal, self.weekday)


    def json(self):

        return {
            'id' : self.job_id,
            'custID' : self.cust_id,
            'crewID' : self.crew_id,
        }


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
