import typing as t
from time import time
import string
import random

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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


    def add_job(self, name: str, address: str, date_timestamp: float, notes: str):

        j = Job(name=name, address=address, account_id=self.id,
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
    account: Account = db.relationship('Account', backref='customers')


    def __init__(self, address: str, contact_name: str,
                 phone_number: str, notes: str, account_id: int):

        self.address = address
        self.cust_id = 'cus_' + gen_id()
        self.contact_name = contact_name
        self.notes = notes
        self.account_id = account_id
        self.phone_number = phone_number


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

    account: Account = db.relationship('Account', backref='crews')
    jobs: t.List['Job'] = db.relationship('Job', secondary=job_table, back_populates='crews')
    members: t.List['User'] = db.relationship('User', secondary=crew_table, back_populates='crews')


    def __init__(self, name: str, description: str, account_id: int):

        self.name = name
        self.account_id = account_id
        self.description = description
        self.crew_id = 'crew_' + gen_id()


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

        db.session.delete(self)
        db.session.commit()


class Job(db.Model):

    __tablename__ = 'jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String, index=True)

    name: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    created_timestamp: float = db.Column(db.Float)
    work_date_timestamp: float = db.Column(db.Float)
    last_updated_timestamp: float = db.Column(db.Float)
    address: str = db.Column(db.String)
    notes: str = db.Column(db.String)

    # Added by the Comment model
    comments: t.List['Comment']

    account = db.relationship('Account', backref='jobs')

    crews: t.List['Crew'] = db.relationship('Crew', secondary=job_table, back_populates='jobs')


    def __init__(self, name: str, account_id: int, address: str, notes: str, work_date_timestamp: float):

        self.name = name
        self.account_id = account_id
        self.work_date_timestamp = work_date_timestamp
        now = time() * 1000 # Convert to milliseconds to make working with frontend easier
        self.created_timestamp = now
        self.last_updated_timestamp = now
        self.job_id = 'job_' + gen_id()
        self.address = address
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
            'workDateTimestamp' : self.work_date_timestamp,
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

        db.session.delete(self)
        db.session.commit()


class DailyJob(db.Model):

    __tablename__ = 'daily_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String)
    cust_id: int = db.Column(db.Integer)
    notes: str = db.Column(db.String)
    # Indices of months (0-Jan, 1-Feb, etc...)
    start_month: db.Column(db.Integer)
    end_month: db.Column(db.Integer)


    def __init__(self, cust_id: int,
                 start_month: int,
                 end_month: int):

        self.job_id = f'dailyjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_month = start_month
        self.end_month = end_month


    def delete(self):

        db.session.delete(self)
        db.session.commit()


class WeeklyJob(db.Model):

    __tablename__ = 'weekly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String)
    cust_id: int = db.Column(db.Integer)
    notes: str = db.Column(db.String)

    sunday: db.Column(db.Boolean)
    monday: db.Column(db.Boolean)
    tuesday: db.Column(db.Boolean)
    wednesday: db.Column(db.Boolean)
    thursday: db.Column(db.Boolean)
    friday: db.Column(db.Boolean)
    saturday: db.Column(db.Boolean)

    # Indices of months (0-Jan, 1-Feb, etc...)
    start_month: db.Column(db.Integer)
    end_month: db.Column(db.Integer)


    def __init__(self, cust_id: int,
                 sunday: bool, monday: bool,
                 tuesday: bool, wednesday: bool,
                 thursday: bool, friday: bool,
                 saturday: bool, start_month: int,
                 end_month: int):

        self.job_id = f'weekjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_month = start_month
        self.end_month = end_month

        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday


    def delete(self):

        db.session.delete(self)
        db.session.commit()


class MonthlyJob(db.Model):

    __tablename__ = 'monthly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String)
    cust_id: int = db.Column(db.Integer)
    notes: str = db.Column(db.String)

    sunday: db.Column(db.Boolean)
    monday: db.Column(db.Boolean)
    tuesday: db.Column(db.Boolean)
    wednesday: db.Column(db.Boolean)
    thursday: db.Column(db.Boolean)
    friday: db.Column(db.Boolean)
    saturday: db.Column(db.Boolean)

    # Indices of months (0-Jan, 1-Feb, etc...)
    start_month: db.Column(db.Integer)
    end_month: db.Column(db.Integer)

    # Every 2 weeks, every 3 weeks, etc...
    num_of_weeks: int = db.Column(db.Integer)

    def __init__(self, cust_id: int,
                 sunday: bool, monday: bool,
                 tuesday: bool, wednesday: bool,
                 thursday: bool, friday: bool,
                 saturday: bool, start_month: int,
                 end_month: int, num_of_weeks: int):

        self.job_id = f'monthjob_{gen_id(18)}'

        self.cust_id = cust_id
        self.start_month = start_month
        self.end_month = end_month
        self.num_of_weeks = num_of_weeks

        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday


    def delete(self):

        db.session.delete(self)
        db.session.commit()


class YearlyJob(db.Model):

    __tablename__ = 'yearly_jobs'

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String)
    cust_id: int = db.Column(db.Integer)
    notes: str = db.Column(db.String)

    # Indices of months (0-Jan, 1-Feb, etc...)
    month: int = db.Column(db.Integer)

    # Every 2 weeks, every 3 weeks, etc...
    num_of_weeks: int = db.Column(db.Integer)

    def __init__(self, cust_id: int, notes: str,
                 start_month: int, end_month: int,
                 num_of_weeks: int):

        self.job_id = f'yearjob_{gen_id(18)}'
        self.cust_id = cust_id
        self.notes = notes
        self.start_month = start_month
        self.end_month = end_month
        self.num_of_weeks = num_of_weeks


    def delete(self):

        db.session.delete(self)
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


def create_account(email: str, password: str):

    a = Account(email=email)
    a.save()
    a.add_user(email=email, phone_number='', password=password, is_admin=True)
    return a
