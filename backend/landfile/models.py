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
    db.Column('crew_id', db.Integer, db.ForeignKey('crew.id')),
)

crew_leads = db.Table(
    'crew_leads',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('crew_id', db.Integer(), db.ForeignKey('crew.id')),
)

job_table = db.Table(
    'crew_jobs',
    db.Column('crew_id', db.Integer(), db.ForeignKey('crew.id')),
    db.Column('job_id', db.Integer(), db.ForeignKey('jobs.id')),
)

def gen_id(size=14, chars=string.ascii_letters + string.digits):
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.choice(chars) for _ in range(size))


class Account(db.Model):

    __tablename__ = 'accounts'

    id: int = db.Column(db.Integer, primary_key=True)
    acc_id: str = db.Column(db.String, index=True)
    username: str = db.Column(db.String)

    # This is a json field
    stripe_payment_method_info: str = db.Column(db.String)

    stripe_subscription_id: str = db.Column(db.String)
    stripe_payment_method_id: str = db.Column(db.String)
    seats: int = db.Column(db.Integer)
    plan: str = db.Column(db.String)

    admins: t.List['User']
    members: t.List['User']
    jobs: t.List['Job']

    def __init__(self, username: str):

        self.username = username
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


    def add_user(self, email: str, password: str):

        u = User(
            password=password,
            email=email,
            account_id=self.id,
        )

        u.save()

        return u


    def add_group(self, name: str):

        c = Group(name=name, account_id=self.id)
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


class User(db.Model):

    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: str = db.Column(db.String, index=True)

    email: str = db.Column(db.String, unique=True)
    password: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    account: Account = db.relationship('Account', backref='members')
    crew_leads: t.List['Crew'] = db.relationship('Crew', secondary=crew_table, back_populates='leads')
    crew: t.List['Crew']  = db.relationship('Crew', secondary=crew_leads, back_populates='members')
    _account: Account = db.relationship('Account', backref='admins')


    def __init__(self, email: str, password: str, account_id: int):

        self.user_id = 'user_' + gen_id()
        self.password = generate_password_hash(password)
        self.email = email
        self.account_id = account_id


    def verify(self, password: str):

        return check_password_hash(self.password, password)


    def save(self):

        db.session.add(self)
        db.session.commit()


    def is_account_admin(self):

        return self in self.account.admins


class Crew(db.Model):

    __tablename__ = 'crews'

    id: int = db.Column(db.Integer, primary_key=True)
    crew_id: str = db.Column(db.String, index=True)

    name: str = db.Column(db.String)
    account_id: int = db.Column(db.Integer)

    account: Account = db.relationship('Account', backref='crews')
    jobs: t.List['Job'] = db.relationship('Crew', secondary=job_table, back_populates='crews')
    leads: t.List['User'] = db.relationship('User', secondary=crew_leads, back_populates='crew_leads')
    members: t.List['User'] = db.relationship('User', secondary=crew_table, back_populates='crew')


    def __init__(self, name: str, account_id: int):

        self.name = name
        self.account_id = account_id
        self.user_id = 'crew_' + gen_id()


    def save(self):

        db.session.add(self)
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

    account = db.relationship('Account', backref='jobs')
    crew: t.List['Crew'] = db.relationship('Crew', secondary=job_table, back_populates='jobs')


    def __init__(self, name: str, account_id: int, work_date_timestamp: float):

        self.name = name
        self.account_id = account_id
        self.work_date_timestamp = work_date_timestamp
        now = time()
        self.created_timestamp = now
        self.last_updated_timestamp = now
        self.job_id = 'job_' + gen_id()


    def save(self):

        db.session.add(self)
        db.session.commit()


def create_account(email: str, password: str):

    a = Account(primary_email=email)
    a.save()
    a.add_user(email=email, password=password)
