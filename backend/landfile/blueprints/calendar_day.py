from flask import Blueprint, request, abort, jsonify

from flask_jwt_extended import jwt_required

from landfile.models import User

calendar_day = Blueprint('calendar_day', 'calendar_day', url_prefix='/calendar/<year:int>/<month:int>/<day:int>')


def get_account():

    u: User = User.query.all()[0]

    return u.account


@calendar_day.route('', methods=['GET'])
# @jwt_required
def get_jobs(year: int, month: int, day: int):

    acc = get_account()

    return jsonify([c.json() for c in acc.calendar_day])


@calendar_day.route('', methods=['POST'])
# @jwt_required
def add_customer():

    acc = get_account()

    js = request.json

    acc.add_customer(address=js['address'], contact_name=js['name'], phone_number=js['phoneNumber'], notes='')

    return {}
